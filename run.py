from flask import Flask, render_template
from app.main_routes import main_bp
from app.admin_routes import admin_bp
from app.scheduler import init_scheduler

app = Flask(__name__)
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.config.from_object("app.config.Config")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    init_scheduler()
    app.run(host="0.0.0.0", debug=False)
