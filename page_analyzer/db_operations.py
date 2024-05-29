from psycopg2.extras import NamedTupleCursor
from psycopg2 import DatabaseError
import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort)
from dotenv import load_dotenv
from urllib.parse import urlparse
from psycopg2.extras import NamedTupleCursor
from page_analyzer.validator import validate_url
from bs4 import BeautifulSoup

import os
import psycopg2
import datetime
import requests


def execute_query(connection, query, params=None, is_select=False):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(query, params or ())
        if is_select:
            return cursor.fetchall()
        connection.commit()


def fetch_urls(connection):
    return execute_query(connection, """
        SELECT DISTINCT ON (urls.id)
            urls.id,
            urls.name,
            url_checks.status_code,
            url_checks.created_at
        FROM urls LEFT JOIN url_checks
        ON urls.id = url_checks.url_id
        ORDER BY urls.id DESC;
    """, is_select=True)


def insert_url(connection, normalized_url):
    url_id = execute_query(connection, """
        INSERT INTO urls (name, created_at) VALUES (%s, %s)
        RETURNING id;
    """, (normalized_url, datetime.datetime.now()), is_select=True)
    if url_id:
        flash('Страница успешно добавлена', 'success')
        return url_id[0].id
    else:
        flash('Ошибка при добавлении страницы', 'danger')
        return redirect(url_for('index'))


def fetch_url_and_checks(connection, url_id):
    url = execute_query(connection, """
        SELECT * FROM urls WHERE id=%s;
    """, (url_id,), is_select=True)
    checks = execute_query(connection, """
        SELECT * FROM url_checks WHERE url_id=%s ORDER BY id ASC;
    """, (url_id,), is_select=True)
    return url, checks


def fetch_url(connection, url_id):
    return execute_query(connection, """
        SELECT * FROM urls WHERE id=%s;
    """, (url_id,), is_select=True)


def insert_check(connection, url_id, site_content):
    execute_query(connection, """
        INSERT INTO url_checks
        (url_id, created_at, status_code, h1, title, description)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (url_id, datetime.datetime.now(), site_content['status_code'],
          site_content['h1'], site_content['title'],
          site_content['description']))