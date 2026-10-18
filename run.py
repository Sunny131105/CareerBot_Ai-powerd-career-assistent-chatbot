"""Run CareerBot: python run.py"""
import threading
import time
import webbrowser

from server import app


def main():
    print("Starting CareerBot on http://127.0.0.1:5000  (Ctrl+C to stop)")
    threading.Thread(
        target=lambda: app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False),
        daemon=True,
    ).start()
    time.sleep(2)
    try:
        webbrowser.open('http://127.0.0.1:5000')
    except Exception:
        pass
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")


if __name__ == "__main__":
    main()
