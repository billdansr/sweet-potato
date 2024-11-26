from apiflask import APIFlask


app = APIFlask(__name__, docs_ui='swagger-ui', title='Sweet Potato API', version='1.0.0')
app.config['SPEC_FORMAT'] = 'json'
app.config['LOCAL_SPEC_PATH'] = 'openapi.json'
app.config['SYNC_LOCAL_SPEC'] = True
app.config['LOCAL_SPEC_JSON_INDENT'] = 4

@app.get('/')
def index():
    return {'message': 'hello'}