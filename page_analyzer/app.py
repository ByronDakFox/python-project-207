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
import validators
import psycopg2
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def create_url():

    url = request.form.get('url')

    errors=[]

    if not validators.url(url):
        errors.append('URL inválida')

    if len(url) > 255:
        errors.append(
            'Debe tener menos de 255 caracteres'
        )

    if errors:

        for error in errors:
            flash(error,'danger')

        return render_template(
            'index.html',
            url=url
        ),422

    parsed_url=urlparse(url)

    normalized=(
        f'{parsed_url.scheme}://'
        f'{parsed_url.netloc}'
    )

    conn=get_connection()

    cur=conn.cursor()

    cur.execute(
        "SELECT id FROM urls WHERE name=%s",
        (normalized,)
    )

    existing=cur.fetchone()

    if existing:

        flash(
            'La URL ya existe',
            'warning'
        )

        conn.close()

        return redirect(
            url_for(
                'show_url',
                id=existing[0]
            )
        )

    cur.execute(
        """
        INSERT INTO urls
        (name,created_at)
        VALUES(%s,%s)
        RETURNING id
        """,
        (
            normalized,
            datetime.now()
        )
    )

    url_id=cur.fetchone()[0]

    conn.commit()

    conn.close()

    flash(
        'URL agregada correctamente',
        'success'
    )

    return redirect(
        url_for(
            'show_url',
            id=url_id
        )
    )


@app.route('/urls')
def urls():

    conn=get_connection()

    cur=conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM urls
        ORDER BY id DESC
        """
    )

    urls=cur.fetchall()

    conn.close()

    return render_template(
        'urls.html',
        urls=urls
    )


@app.route('/urls/<int:id>')
def show_url(id):

    conn=get_connection()

    cur=conn.cursor()

    cur.execute(
        "SELECT * FROM urls WHERE id=%s",
        (id,)
    )

    url=cur.fetchone()

    conn.close()

    return render_template(
        'url.html',
        url=url
    )