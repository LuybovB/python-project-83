from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
port = int(os.environ.get("PORT", 8000))


@app.route("/")
def index():
    app.logger.info("Processing request to root URL")
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
