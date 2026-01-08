# main.py

from dotenv import load_dotenv
import threading


def run_flask():
    """Start the Flask server."""
    from flask_app import app

    app.run(host="0.0.0.0", port=3000)


def main():
    """Entry point of the application."""
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    load_dotenv()


if __name__ == "__main__":
    main()
