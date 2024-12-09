from apiflask import APIFlask
from flask_cors import CORS
from db import close_connection, query_db


app = APIFlask(__name__, docs_ui='swagger-ui', title='Sweet Potato API', version='1.0.0')

app.config['SPEC_FORMAT'] = 'json'
app.config['LOCAL_SPEC_PATH'] = 'openapi.json'
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_JSON_INDENT'] = 4

app.teardown_appcontext(close_connection)

CORS(app)


@app.get('/api/')
def index_api():
    return {'message': 'hello'}
