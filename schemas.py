from marshmallow import Schema, fields, validate

class ProfileSchema(Schema):
    id = fields.Int(dump_only = True)
    single_id = fields.Int(dump_only = True, required = True)
    location = fields.Str(required = True)
    bio = fields.Str(required = True, validate=validate.Length(max=150))
    five_interests = fields.Str(validate=validate.Length(max=50))
    seeking = fields.Str(validate=validate.Length(max=50))
    last_login = fields.Str(dump_only=True)

class SingleSchema(Schema):
    id = fields.Str(dump_only = True)
    username = fields.Str(required = True, validate=validate.Length(max=30))
    email = fields.Str(required = True)
    password = fields.Str(required = True, load_only = True)
    first_name = fields.Str()
    last_name = fields.Str()
    age = fields.Int(required=True)
    orientation = fields.Str()
    height = fields.Str()
    astrological_sign = fields.Str()
  
class SingleSchemaNested(SingleSchema):
    profile = fields.List(fields.Nested(ProfileSchema), dump_only=True)
    liked = fields.List(fields.Nested(SingleSchema), dump_only=True)

class UpdateSingleSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(required = True, load_only = True)
    new_password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    age = fields.Int()
    orientation = fields.Str()
    height = fields.Str()
    astrological_sign = fields.Str()

class AuthSingleSchema(Schema):
  username = fields.Str(required=True) #Required maybe not necessary? Check back.
  email = fields.Str()
  password = fields.Str(required = True, load_only = True)