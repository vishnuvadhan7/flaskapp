from flask import Flask
from config import Config

from app.routes.employee import employee_bp
from app.routes.department import department_bp
from app.routes.home import home_bp

from app.models import db

from flask_migrate import Migrate

migrate = Migrate()

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    #initialize database
    db.init_app(app)

    #flask migrate
    migrate.init_app(app,db)
    
    app.register_blueprint(home_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(department_bp)

    return app


