from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from resources.singles.SingleModel import SingleModel

from .ProfileModel import ProfileModel
from schemas import ProfileSchema, UpdateProfileSchema
from . import bp


@bp.route('/')
class ProfileList(MethodView):
  
    # @jwt_required()
    @bp.response(200, ProfileSchema(many=True))
    def get(self):
        return ProfileModel.query.all()

    @jwt_required()
    @bp.arguments(ProfileSchema)
    @bp.response(200, ProfileSchema)
    def post(self, profile_data):
        single_id = get_jwt_identity()
        p = ProfileModel(**profile_data, single_id = single_id)
        try:
            p.save()
            return p
        except IntegrityError:
            abort(400, message="Invalid Single ID")

@bp.route('/<profile_id>')
class Profile(MethodView):
  
    @jwt_required()
    @bp.response(200, ProfileSchema)
    def get(self, profile_id):
        p = ProfileModel.query.get(profile_id)
        if p:
            return p
        abort(400, message='Invalid Profile ID')

    @jwt_required()
    @bp.arguments(UpdateProfileSchema)
    @bp.response(200, UpdateProfileSchema)
    def put(self, profile_data,profile_id):
        p = ProfileModel.query.get(profile_id)
        if p: #Could add something here like "if p and profile_data['body']", but nothing will really guaranteed change for this
            single_id = get_jwt_identity()
            if p.single_id == single_id:
                if 'location' in profile_data:
                    p.location = profile_data['location']
                if 'bio' in profile_data:
                    p.bio = profile_data['bio']
                if 'five_interests' in profile_data:
                    p.five_interests = profile_data['five_interests']
                if 'seeking' in profile_data:
                    p.seeking = profile_data['seeking']
                p.save()
                return p
            else:
                abort(401, message='Unauthorized')
                abort(400, message='Invalid Post Data')

    @jwt_required()
    def delete(self, profile_id):
        single_id = get_jwt_identity()
        p = ProfileModel.query.get(profile_id)
        if p:
            if p.single_id == single_id:
                p.delete()
                return {'message' : 'Profile Deleted'}, 202
            abort(401, message='Singleton does not have rights')
        abort(400, message='Invalid Profile ID')