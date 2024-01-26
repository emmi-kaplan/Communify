from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('profile_model.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('profile_model.id'), primary_key=True)
)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    liked_posts = db.relationship('PostModel', backref='liker', lazy=True)
    posts = db.relationship('PostModel', backref='author', lazy=True)
    followers = db.relationship(
        'ProfileModel', secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref=db.backref('following', lazy='dynamic'), lazy='dynamic'
    )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('profile_model.id'), nullable=False)
    reactions = db.relationship('ReactionModel', backref='post', lazy=True)
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Reaction(db.Model):
    class Emotion(str, Enum):
        like = 'like'
        love = 'love'
        hate = 'hate'
        uncomfortable = 'uncomfortable'
        boring = 'boring'
    comment = db.Column(db.Text, nullable=True)
    emote = db.Column(Emotion, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('profile_model.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post_model.id'), nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # in order to react, you must either comment or emote
    @validates('comment', 'emote')
    def validate_comment_or_emote(self, key, value):
        if self.emote is None and self.comment is None:
            raise ValueError("Either 'comment' or 'emote' must be provided.")
        return value

