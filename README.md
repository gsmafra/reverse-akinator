# Reverse Akinator

Akinator, but you're guessing the character.

Play here: https://reverse-akinator.onrender.com/

## How to run locally

Create a virtualenv, preferably with Python 3.11, then activate. Other versions are not tested. Install requirements:
```
pip install -r requirements.txt
```

Set environment variables listed in `app/config.py`. You will need to have accounts for Google AI and Firebase. Both have free plans. Sentry is optional.

Then launch the app:
```
python run.py
```

Access locally on http://127.0.0.1:5000/
