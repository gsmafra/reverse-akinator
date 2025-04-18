import os
import atexit
import requests
from apscheduler.schedulers.background import BackgroundScheduler

# Use an environment variable for the base URL, default to localhost for development
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000")
PING_URL = f"{BASE_URL}/ping"


def scheduled_ping():
    try:
        response = requests.get(PING_URL, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        print("Scheduled ping response:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error during scheduled ping: {e}")


def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=scheduled_ping, trigger="interval", minutes=14)
    scheduler.start()
    atexit.register(scheduler.shutdown)
