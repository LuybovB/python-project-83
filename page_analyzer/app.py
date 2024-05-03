from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
port = int(os.environ.get("PORT", 8000))


@app.route("/")
def index():
    app.logger.info("Processing request to root URL")
    return render_template("index.html")


@app.route("/url", methods=["POST"])
def add_url():
    name = request.form['name']
    created_at = datetime.now()

    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cur = conn.cursor()

    cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)", (name, created_at))
    conn.commit()

    cur.close()
    conn.close()

    return "URL added successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
