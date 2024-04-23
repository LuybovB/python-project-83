from flask import Flask
import os


app = Flask(__name__)

# Retrieve the PORT environment variable or use 5000 as a default
port = int(os.environ.get("PORT", 8000))


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    # Run the app on the specified port
    app.run(host="0.0.0.0", port=port)
