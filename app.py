import os
from apiflask import APIFlask, HTTPTokenAuth
from db import close_connection
from flask_cors import CORS
from routes import *


app = APIFlask(__name__, docs_ui='swagger-ui', title='Sweet Potato API', version='1.0.0')
auth = HTTPTokenAuth(scheme='Bearer')

app.config.from_prefixed_env()
app.config['SPEC_FORMAT'] = 'json'
app.config['LOCAL_SPEC_PATH'] = os.path.join(app.root_path, 'openapi.json')
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_JSON_INDENT'] = 4
app.config['UPLOAD_DIR'] = os.path.join(app.root_path, 'upload')

app.teardown_appcontext(close_connection)

CORS(app)

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)

def create_token(user_id):
    # Implement your token creation logic here
    # Return the token
    # Example:
    # token = generate_token(user_id)
    # return token
    header = {'alg': 'HS256'}
    payload = {'id': user_id}
    pass

@auth.verify_token
def verify_token(token):
    # Implement your token verification logic here
    # Return the user ID if the token is valid, otherwise return None
    # Example:
    # user_id = verify_
    pass

# Register routes
init_game_routes(app, auth)
init_genre_routes(app)
init_platform_routes(app)
init_company_routes(app)
init_upload_routes(app)
