from flask_smorest import Blueprint

bp = Blueprint('profiles', __name__, url_prefix='/profile')

from . import routes