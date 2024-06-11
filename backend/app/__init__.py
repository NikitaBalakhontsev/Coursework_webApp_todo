# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
#
# from app.config import Config
#
#
# app = Flask(__name__)
# app.config.from_object(Config)
# CORS(app)  # Разрешить все запросы CORS
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# jwt = JWTManager(app)
#
#
# from app import models, routes

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import Config



db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(category_bp, url_prefix='/api')
    app.register_blueprint(task_bp, url_prefix='/api')
    app.register_blueprint(tag_bp, url_prefix='/api')

    return app

from app.routes.user_routes import user_bp
from app.routes.auth_routes import auth_bp
from app.routes.category_routes import category_bp
from app.routes.task_routes import task_bp
from app.routes.tag_routes import tag_bp