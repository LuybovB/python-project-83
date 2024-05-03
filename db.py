from config import host, user, password, db_name
import psycopg2

connection = None

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version()"
        )

        print(f"Server version: {cursor.fetchone()}")

except Exception as ex:
    print("[INFO] Error:", ex)

finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")