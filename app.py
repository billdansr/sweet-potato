import os
from apiflask import APIFlask
from db import init_app
from flask_cors import CORS
from routes import authentication, company, game, genre, rating, platform, role, user
from flask import send_from_directory

app = APIFlask(__name__, docs_ui='swagger-ui', title='Sweet Potato API', version='1.0.0')

app.config['ENV'] = os.environ.get('ENV', 'production')
app.config['DEBUG'] = os.environ.get('DEBUG', False)
app.config['APP'] = os.environ.get('APP', 'app.py')
app.config['RUN_HOST'] = os.environ.get('RUN_HOST', '0.0.0.0')
app.config['RUN_PORT'] = os.environ.get('RUN_PORT', 5000)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')
app.config['JWT_ALGORITHM'] = os.environ.get('JWT_ALGORITHM', 'HS256')
app.config['SPEC_FORMAT'] = 'json'
app.config['LOCAL_SPEC_PATH'] = os.path.join(app.root_path, 'openapi.json')
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_JSON_INDENT'] = 4
app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')
app.config['UPLOAD_DIR'] = os.path.join(app.instance_path, 'upload')

init_app(app)

# CORS(app)

cors = CORS(app, resources={
    r'/*': {
        'origins': ['*'],
        'supports_credentials': True,
        'send_wildcard': True,
    }
})

# Create directory if it doesn't exist
os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)


# Register routes
@app.get('/upload/<path:filename>')
def read_upload(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)


# Register blueprints
app.register_blueprint(authentication, url_prefix='/auth')
app.register_blueprint(company, url_prefix='/api/companies')
app.register_blueprint(game, url_prefix='/api/games')
app.register_blueprint(genre, url_prefix='/api/genres')
app.register_blueprint(platform, url_prefix='/api/platforms')
app.register_blueprint(rating, url_prefix='/api/ratings')
app.register_blueprint(role, url_prefix='/api/roles')
app.register_blueprint(user, url_prefix='/api/users')

# if __name__ == '__main__':
#     app.run(host=app.config['RUN_HOST'], port=app.config['RUN_PORT'])
