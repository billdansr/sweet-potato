import os
from apiflask import APIFlask
from db import init_app
from flask_cors import CORS
from routes import authentication, company, game, genre, platform, role, user
from flask import send_from_directory

app = APIFlask(__name__, docs_ui='swagger-ui', title='Sweet Potato API', version='1.0.0')

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


# Register routes
@app.get('/upload/<path:filename>')
def read_upload(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)


# Register blueprints
app.register_blueprint(authentication)
app.register_blueprint(company)
app.register_blueprint(game)
app.register_blueprint(genre)
app.register_blueprint(platform)
app.register_blueprint(role)
app.register_blueprint(user)
