from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError

from schemas import ProfileSchema, UpdateSingleSchema, SingleSchema, AuthSingleSchema, SingleSchemaNested
from . import bp
from .SingleModel import SingleModel

@bp.route('/single')
class SingleList(MethodView):  
  
    @bp.response(200, SingleSchema(many = True))
    def get(self):
        singles = SingleModel.query.all()
        return singles

    @jwt_required()
    @bp.arguments(AuthSingleSchema)
    def delete(self, single_data):
        single_id = get_jwt_identity()
        single = SingleModel.query.get(single_id)
        if single and single.username == single_data['username'] and single.check_password(single_data['password']):
            single.delete()
            return {'message':f'{single_data["username"]} deleted'}, 202
        abort(400, message='Username or Password Invalid')

    
    @jwt_required()
    @bp.arguments(UpdateSingleSchema)
    @bp.response(202, SingleSchema)
    def put(self, single_data):
        single_id = get_jwt_identity()
        single = SingleModel.query.get_or_404(single_id, description='Single Not Found')
        if single and single.check_password(single_data['password']):
            try:
                single.from_dict(single_data)
                single.save()
                return single
            except IntegrityError:
                abort(400, message='Username or Email already Taken')

@bp.route('/single/<single_id>')
class Single(MethodView):

  @bp.response(200, SingleSchemaNested)
  def get(self, single_id):
    single = SingleModel.query.get_or_404(single_id, description='Single Not Found')
    return single


@bp.route('/single/like/<liked_id>')
class LikeSingle(MethodView):
  
  @jwt_required()
  @bp.response(200, SingleSchema(many=True))
  def post(self, liked_id):
    liker_id = get_jwt_identity()
    single = SingleModel.query.get(liker_id)
    single_to_like = SingleModel.query.get(liked_id)
    if single and single_to_like:
      single.like_single(single_to_like)
      return single.liked.all()
    abort(400, message='Invalid single info')

  @jwt_required()
  def put(self, liked_id):
    liker_id = get_jwt_identity()
    single = SingleModel.query.get(liker_id)
    single_to_unlike = SingleModel.query.get(liked_id)
    if single and single_to_unlike:
      single.unlike_single(single_to_unlike)
      return {'message': f'Unliked Single: {single_to_unlike.username}'}, 202
    abort(400, message='Invalid single info')  