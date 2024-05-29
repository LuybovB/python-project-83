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
