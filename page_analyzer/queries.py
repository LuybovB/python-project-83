from psycopg2.extras import NamedTupleCursor


def get_all_urls_query(connection):
    query = """SELECT DISTINCT ON (urls.id)
                      urls.id,
                      urls.name,
                      url_checks.status_code,
                      url_checks.created_at
                 FROM urls LEFT JOIN url_checks
                 ON urls.id = url_checks.url_id
                 ORDER BY urls.id DESC;"""
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(query)
        urls = cursor.fetchall()
    return urls
