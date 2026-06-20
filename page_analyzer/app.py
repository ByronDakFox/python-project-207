import os
from datetime import datetime
from urllib.parse import urlparse

import psycopg2
import validators
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort
)

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'secret-key'
)

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def create_url():

    url = request.form.get('url', '').strip()

    errors = {}

    if not url:
        errors['url'] = 'URL requerida'

    elif len(url) > 255:
        errors['url'] = 'URL debe contener menos de 255 caracteres'

    elif not validators.url(url):
        errors['url'] = 'URL inválida'

    if errors:
        flash(
            list(errors.values())[0],
            'danger'
        )

        return render_template(
            'index.html',
            url=url,
            errors=errors
        ), 422

    parsed = urlparse(url)

    normalized_url = (
        f'{parsed.scheme}://{parsed.netloc}'
    )

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        '''
        SELECT id
        FROM urls
        WHERE name = %s
        ''',
        (normalized_url,)
    )

    existing_url = cur.fetchone()

    if existing_url:

        flash(
            'La página ya existe',
            'info'
        )

        cur.close()
        conn.close()

        return redirect(
            url_for(
                'show_url',
                id=existing_url[0]
            )
        )

    cur.execute(
        '''
        INSERT INTO urls
        (
            name,
            created_at
        )
        VALUES
        (
            %s,
            %s
        )
        RETURNING id
        ''',
        (
            normalized_url,
            datetime.now()
        )
    )

    url_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    flash(
        'La página se agregó correctamente',
        'success'
    )

    return redirect(
        url_for(
            'show_url',
            id=url_id
        )
    )


@app.get('/urls')
def urls():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
    '''
    SELECT
        urls.id,
        urls.name,
        url_checks.status_code,
        url_checks.created_at
    FROM urls
    LEFT JOIN (
        SELECT DISTINCT ON (url_id)
            url_id,
            status_code,
            created_at
        FROM url_checks
        ORDER BY url_id, created_at DESC
    ) AS url_checks
        ON urls.id = url_checks.url_id
    ORDER BY urls.id DESC
    '''
)

    urls_list = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        'urls.html',
        urls=urls_list
    )


@app.get('/urls/<int:id>')
def show_url(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        '''
        SELECT *
        FROM urls
        WHERE id = %s
        ''',
        (id,)
    )

    url = cur.fetchone()

    if not url:
        abort(404)

    cur.execute(
        '''
        SELECT *
        FROM url_checks
        WHERE url_id = %s
        ORDER BY id DESC
        ''',
        (id,)
    )

    checks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        'url.html',
        url=url,
        checks=checks
    )


@app.post('/urls/<int:id>/checks')
def create_check(id):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            '''
            SELECT id, name
            FROM urls
            WHERE id = %s
            ''',
            (id,)
        )

        url = cur.fetchone()

        if not url:
            flash('URL no encontrada', 'danger')
            return redirect(url_for('urls'))

        response = requests.get(
            url[1],
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            'html.parser'
        )

        h1 = ''
        h1_tag = soup.find('h1')
        if h1_tag:
            h1 = h1_tag.get_text(strip=True)

        title = ''
        if soup.title:
            title = soup.title.get_text(strip=True)

        description = ''
        description_tag = soup.find(
            'meta',
            attrs={'name': 'description'}
        )

        if description_tag:
            description = description_tag.get(
                'content',
                ''
            )

        h1 = h1[:255]
        title = title[:255]
        description = description[:255]

        cur.execute(
            '''
            INSERT INTO url_checks
            (
                url_id,
                status_code,
                h1,
                title,
                description,
                created_at
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ''',
            (
                id,
                response.status_code,
                h1,
                title,
                description,
                datetime.now()
            )
        )

        conn.commit()

        flash(
            'La página fue verificada correctamente',
            'success'
        )

    except requests.RequestException:
        flash(
            'Ocurrió un error al hacer la verificación',
            'danger'
        )

    finally:
        cur.close()
        conn.close()

    return redirect(
        url_for(
            'show_url',
            id=id
        )
    )