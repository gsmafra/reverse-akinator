import sentry_sdk
from flask import Flask, render_template

from app.routes.main import main_bp
from app.routes.admin import admin_bp
from app.scheduler import init_scheduler
from app.db_access import init_firebase

app = Flask(__name__)
app.db = init_firebase()
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.config.from_object("app.config.Config")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


def init_sentry():
    if app.config["SENTRY_DSN"] is None:
        return
    sentry_sdk.init(dsn=app.config["SENTRY_DSN"], send_default_pii=True, environment=app.config["ENVIRONMENT"])


if __name__ == "__main__":
    init_scheduler()
    init_sentry()
    app.run(host="0.0.0.0", debug=False)
