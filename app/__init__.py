from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from Config import Config
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

from resources.singles import bp as single_bp
api.register_blueprint(single_bp)
from resources.profiles import bp as profile_bp
api.register_blueprint(profile_bp)

from resources.singles import routes
from resources.profiles import routes

from resources.singles.SingleModel import SingleModel
from resources.profiles.ProfileModel import ProfileModel