import os
from apiflask import APIFlask

base_path = os.path.dirname(os.path.dirname(__file__))

app = APIFlask(__name__, title='Sweet Potato API', version='1.0.0')
app.config['SPEC_FORMAT'] = 'json'
app.config['LOCAL_SPEC_PATH'] = os.path.join(base_path, 'openapi.json')
app.config['LOCAL_SPEC_JSON_INDENT'] = 4
app.config['SYNC_LOCAL_SPEC'] = True

@app.get('/')
def index():
    return {'message': 'hello'}