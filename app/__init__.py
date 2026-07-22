from flask import Flask, redirect, url_for   # <-- add redirect and url_for
from config import Config
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mongo.init_app(app)

    from app.routes.home import home_bp
    from app.routes.employee import employee_bp
    from app.routes.department import department_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(department_bp)

    # Root route – redirect to home page
    @app.route("/")
    def index():
        return redirect(url_for("home.home"))

    return app   # <-- make sure this is inside create_app()