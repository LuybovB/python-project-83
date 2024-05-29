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


def fetch_urls(connection):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("""SELECT DISTINCT ON (urls.id)
                                    urls.id,
                                    urls.name,
                                    url_checks.status_code,
                                    url_checks.created_at
                               FROM urls LEFT JOIN url_checks
                               ON urls.id = url_checks.url_id
                               ORDER BY urls.id DESC;""")
        return cursor.fetchall()


def get_or_create_url(connection, normalized_url):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            "SELECT id FROM urls WHERE name=%s;",
            (normalized_url, )
        )
        existed_url = cursor.fetchone()
        if existed_url:
            flash('Страница уже существует', 'info')
            return existed_url.id
        else:
            cursor.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;",
                (normalized_url, datetime.datetime.now())
            )
            new_url_id = cursor.fetchone().id
            flash('Страница успешно добавлена', 'success')
            return new_url_id


def fetch_url_by_id(connection, url_id):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            "SELECT * FROM urls WHERE id=%s;",
            (url_id, )
        )
        return cursor.fetchone()


def fetch_checks_by_url_id(connection, url_id):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            "SELECT * FROM url_checks WHERE url_id=%s ORDER BY id ASC;",
            (url_id,)
        )
        return cursor.fetchall()
