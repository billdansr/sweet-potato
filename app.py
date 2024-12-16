import os
from apiflask import APIFlask, HTTPTokenAuth
from db import init_app
from flask_cors import CORS
from routes import auth, company, game, genre, platform, role
from flask import send_from_directory

app = APIFlask(__name__, docs_ui='swagger-ui', title='Sweet Potato API', version='1.0.0')
auth = HTTPTokenAuth(scheme='Bearer')

app.config.from_prefixed_env()
app.config['SPEC_FORMAT'] = 'json'
app.config['LOCAL_SPEC_PATH'] = os.path.join(app.root_path, 'openapi.json')
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_JSON_INDENT'] = 4
app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')
app.config['UPLOAD_DIR'] = os.path.join(app.instance_path, 'upload')

init_app(app)

CORS(app)

# Create directory if it doesn't exist
os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)


def create_token(user_id):
    # Implement your token creation logic here
    # Return the token
    # Example:
    # token = generate_token(user_id)
    # return token
    # header = {'alg': 'HS256'}
    # payload = {'id': user_id}
    pass


@auth.verify_token
def verify_token(token):
    # Implement your token verification logic here
    # Return the user ID if the token is valid, otherwise return None
    # Example:
    # user_id = verify_
    pass


# Register routes
@app.get('/upload/<path:filename>')
def read_upload(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)


# Register blueprints
# app.register_blueprint(auth)
app.register_blueprint(company)
app.register_blueprint(game)
app.register_blueprint(genre)
app.register_blueprint(platform)
app.register_blueprint(role)