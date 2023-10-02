from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from schemas import AuthSingleSchema, SingleSchema
from . import bp
from .SingleModel import SingleModel

@bp.post('/register')
@bp.arguments(SingleSchema)
@bp.response(201, SingleSchema)
def register(single_data):
    single = SingleModel()
    single.from_dict(single_data)
    try:
        single.save()
        return single_data
    except IntegrityError:
        abort(400, message='Username or Email already Taken')

@bp.post('/login')
@bp.arguments(AuthSingleSchema)
def login(login_info):
    if 'username' not in login_info and 'email' not in login_info:
        abort(400, message='Please include Username or Email')
    if 'username' in login_info:
        single = SingleModel.query.filter_by(username=login_info['username']).first()
    else:
        single = SingleModel.query.filter_by(email=login_info['email']).first()
    if single and single.check_password(login_info['password']):
        access_token = create_access_token(identity=single.id)
        return {'access_token':access_token}
    abort(400, message='Invalid Username Or Password')
  



# @bp.route('/logout')