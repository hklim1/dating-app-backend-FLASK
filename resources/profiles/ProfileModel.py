from app import db
from datetime import datetime

class ProfileModel(db.Model):

    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key = True)
    single_id = db.Column(db.Integer, db.ForeignKey('singles.id'), nullable = False)
    location = db.Column(db.String, nullable = False)
    bio = db.Column(db.String(150), default="Nothing to see here.")
    five_interests = db.Column(db.String(50))
    seeking = db.Column(db.String(50))
    last_login = db.Column(db.String, default = datetime.utcnow)

    def __repr__(self):
        return f'<Profile: {self.bio}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit() 