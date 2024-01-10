from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ProfileModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    liked_posts = db.relationship('PostModel', backref='liker', lazy=True)
    posts = db.relationship('PostModel', backref='author', lazy=True)
    # i need to learn how to reference a model inside itself
    followers = db.Column(db.String(128), nullable=False)
    following = db.Column(db.String(128), nullable=False)


class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('profile_model.id'), nullable=False)
    reactions = db.relationship('ReactionModel', backref='post', lazy=True)
    # im sure there's a trick for this too
    time_stamp = db.Column(db.String(255), nullable=False)


class ReactionModel(db.Model):
    # this should be an enum
    emotion = ['like', 'love', 'hate', 'uncomfortable', 'boring']
    # is this the best way to have a reaction be either comment or emotion
    # should I add validation so you can't react with no comment or emotion
    comment = db.Column(db.Text, nullable=True)
    emote = db.Column(emotion, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('profile_model.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post_model.id'), nullable=False)
    # im sure there's a trick for this too
    time_stamp = db.Column(db.String(255), nullable=False)
