from flask import Flask
from models import db

# Can create other configs here or in config file
class DevelopmentConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # Enable automatic tracking of modifications
    JWT_SECRET_KEY = 'sneaky-snake'
    #i like this mans smell


app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

# Initialize the db with the app
db.init_app(app)

# Import and Register Blueprints
from endpoints.profile import user_bp
user_bp.db = db
app.register_blueprint(user_bp, url_prefix='/user')

from endpoints.auth import auth_bp
auth_bp.db = db
app.register_blueprint(auth_bp, url_prefix='/auth')

# Create the tables inside application context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)