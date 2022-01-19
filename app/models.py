from app import db
from werkzeug.security import generate_password_hash, check_password_hash

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True)
    nickname = db.Column(db.String(70), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(130))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Usuario {}>'.format(self.username)

    def as_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'email': self.email,
            'password_hash': self.password_hash
        }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(180), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Postagem {}>'.format(self.message)

    def as_dict(self):
        return {
            'id': self.id,
            'message': self.username
        }
