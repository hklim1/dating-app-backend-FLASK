from flask_smorest import Blueprint

bp = Blueprint('singles', __name__, description='Ops on Singles')

from . import routes
from . import auth_routes