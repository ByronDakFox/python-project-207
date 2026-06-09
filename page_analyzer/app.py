from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import datetime

import psycopg2
import validators
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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

    if not validators.url(url):
        errors['url'] = 'URL inválida'

    if len(url) > 255:
        errors['url'] = 'Debe contener menos de 255 caracteres'

    if errors:
        flash('URL inválida', 'danger')

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
        'SELECT id FROM urls WHERE name = %s',
        (normalized_url,)
    )

    existing = cur.fetchone()

    if existing:
        conn.close()

        flash(
            'La página ya existe',
            'info'
        )

        return redirect(
            url_for(
                'show_url',
                id=existing[0]
            )
        )

    cur.execute(
        '''
        INSERT INTO urls
        (name, created_at)
        VALUES (%s, %s)
        RETURNING id
        ''',
        (
            normalized_url,
            datetime.now()
        )
    )

    url_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    flash(
        'Página agregada correctamente',
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
            MAX(url_checks.created_at),
            urls.created_at
        FROM urls
        LEFT JOIN url_checks
        ON urls.id = url_checks.url_id
        GROUP BY urls.id
        ORDER BY urls.id DESC
        '''
    )

    urls = cur.fetchall()

    conn.close()

    return render_template(
        'urls.html',
        urls=urls
    )


@app.get('/urls/<int:id>')
def show_url(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        'SELECT * FROM urls WHERE id = %s',
        (id,)
    )

    url = cur.fetchone()

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

    cur.execute(
        '''
        INSERT INTO url_checks
        (url_id, created_at)
        VALUES (%s, %s)
        ''',
        (
            id,
            datetime.now()
        )
    )

    conn.commit()
    conn.close()

    flash(
        'Página revisada correctamente',
        'success'
    )

    return redirect(
        url_for(
            'show_url',
            id=id
        )
    )