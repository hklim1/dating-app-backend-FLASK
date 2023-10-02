from app import db

from werkzeug.security import generate_password_hash, check_password_hash

likes = db.Table('likes',
    db.Column('liker_id', db.Integer, db.ForeignKey('singles.id')),
    db.Column('liked_id', db.Integer, db.ForeignKey('singles.id'))           
)

class SingleModel(db.Model):

    __tablename__  = 'singles'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password_hash = db.Column(db.String, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    orientation = db.Column(db.String)
    height = db.Column(db.String)
    astrological_sign = db.Column(db.String)
    profile = db.relationship('ProfileModel', backref='user', lazy='dynamic', cascade='all, delete')
    liked = db.relationship('SingleModel', 
        secondary=likes, 
        primaryjoin = likes.c.liker_id == id,
        secondaryjoin = likes.c.liked_id == id,
        backref = db.backref('likers', lazy='dynamic'),
        lazy='dynamic' 
    )

    def __repr__(self):
        return f'<Single: {self.first_name} {self.last_name}, Username: {self.username}>'
  
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
  
    def from_dict(self, dict):
        password = dict.pop('password')
        self.hash_password(password)
        for k,v in dict.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def matched(self, single):
        return self.liked.filter(single.id == likes.c.liked_id).count() > 0
  
    def like_single(self, single):
        if not self.matched(single):
            self.liked.append(single)
            self.save()

    def unlike_single(self, single):
        if self.matched(single):
            self.liked.remove(single)
            self.save()