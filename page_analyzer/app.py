from flask import Flask, render_template
from dotenv import load_dotenv
import psycopg2
import os



load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'dev-secret-key'
)

@app.route('/')
def index():
    return render_template('index.html')