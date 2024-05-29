from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    current_app,
    abort)
from dotenv import load_dotenv
from urllib.parse import urlparse
from psycopg2.extras import NamedTupleCursor
from page_analyzer.validator import validate_url
from bs4 import BeautifulSoup
from .db_operations import fetch_urls, get_or_create_url, fetch_url_by_id, fetch_checks_by_url_id, select_url, insert_url_check


import os
import psycopg2
import datetime
import requests


app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    connection = database_connect()
    urls = fetch_urls(connection)
    connection.close()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def add_url():
    url = request.form.to_dict().get('url')
    error_messages = validate_url(url)
    if error_messages:
        flash(error_messages[0], 'danger')
        return render_template('index.html', url=url), 422

    normalized_url = normalize(url)
    connection = database_connect()
    current_id = get_or_create_url(connection, normalized_url)
    connection.close()
    return redirect(url_for('get_url', id=current_id), 302)


@app.route('/urls/<int:id>')
def get_url(id):
    connection = database_connect()
    try:
        url = fetch_url_by_id(connection, id)
        if not url:
            abort(404, description='Страница не найдена')
        checks = fetch_checks_by_url_id(connection, id)
        return render_template('url.html', url=url, checks=checks)
    except Exception as e:
        current_app.logger.error(f'Ошибка при получении URL или проверок: {e}')
        abort(500, description='Внутренняя ошибка сервера')
    finally:
        connection.close()


@app.errorhandler(503)
@app.errorhandler(404)
def resource_not_found(error):
    return render_template(
        '404_not_found.html',
        error_message=error.description
    ), error.response


@app.template_filter()
def format_timestamp(datetime):
    return datetime.strftime('%Y-%m-%d') if datetime else ''


def database_connect():
    try:
        connection = psycopg2.connect(DATABASE_URL)
        connection.autocommit = True
        return connection
    except psycopg2.DatabaseError or psycopg2.OperationalError:
        abort(503, description='Ошибка доступа к базе данных', response=503)


def normalize(url):
    url = urlparse(url)
    return f'{url.scheme}://{url.netloc}'


def get_site_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        page = BeautifulSoup(response.text, 'html.parser')
        description = page.find('meta', attrs={'name': 'description'})
        site_content = {
            'status_code':
                response.status_code,
            'h1':
                page.find('h1').text if page.find('h1') else '',
            'title':
                page.find('title').text if page.find('title') else '',
            'description':
                description['content'] if description else ''
        }
        return site_content
    except requests.exceptions.RequestException:
        return False


@app.post('/urls/<int:id>/checks')
def check_url(id):
    connection = database_connect()
    try:
        with connection:
            with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
                url = select_url(cursor, id)
                if not url:
                    flash('URL не найден', 'danger')
                    return redirect(url_for('get_url', id=id), 302)

                site_content = get_site_content(url.name)
                if not site_content:
                    flash('Произошла ошибка при проверке', 'danger')
                else:
                    insert_url_check(cursor, id, site_content)
                    flash('Страница успешно проверена', 'success')
            connection.commit()
    except Exception as e:
        connection.rollback()
        flash('Произошла ошибка при работе с базой данных', 'danger')
    finally:
        connection.close()
    return redirect(url_for('get_url', id=id), 302)
