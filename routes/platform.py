from apiflask import APIBlueprint, abort
from db import query_db
from flask import url_for
from routes import auth
from schemas import PlatformIn, PlatformOut, PlatformsOut, EmptySchema, CreatedSchema, AuthorizationHeader

platform = APIBlueprint('platform', __name__, url_prefix='/api/platforms')


@platform.post('/')
@platform.auth_required(auth)
@platform.doc(description='Create a platform', responses=[201, 409])
@platform.input(AuthorizationHeader, location='headers')
@platform.input(PlatformIn, location='json', example=PlatformIn.example())
@platform.output(CreatedSchema, 201, example=CreatedSchema.example())
def create_platform(json_data):
    platform_id = query_db('INSERT INTO "platforms" ("name") VALUES (?);', (json_data['name'],)) if not query_db('SELECT "name" FROM "platforms" WHERE "name" = ? LIMIT 1;', (json_data['name'],), one=True) else abort(409, detail={"field": "name", "issue": f"Platform already exists: {json_data['name']}"})
    query_db('COMMIT;')
    return {'message': 'Platform created successfully!', 'id': platform_id}, 201


@platform.get('/')
@platform.doc(description='Retrieve list platforms', responses=[200, 404])
@platform.output(PlatformsOut(many=True), 200, example=PlatformsOut.example())
def read_platforms():
    results = [dict(result) for result in query_db('SELECT * FROM "platforms"')] or abort(404, detail='Platforms not found')

    for result in results:
        result['url'] = url_for('platform.read_platform', id=result['id'], _external=True)
        del result['id']
    
    return results, 200


@platform.get('/<int:id>')
@platform.doc(description='Single platform', responses=[200, 404])
@platform.output(PlatformOut, 200, example=PlatformOut.example())
def read_platform(id):
    result = dict(query_db('SELECT * FROM "platforms" WHERE "id" = ?', (id,), one=True) or abort(404, detail='Platform not found'))
    return result, 200


@platform.patch('/<int:id>')
@platform.auth_required(auth)
@platform.doc(description='Update a platform', responses=[204, 404])
@platform.input(AuthorizationHeader, location='headers')
@platform.input(PlatformIn, location='json', example=PlatformIn.example())
@platform.output(EmptySchema, 204)
def update_platform(id, json_data):
    query_db('UPDATE "platforms" SET "name" = ? WHERE "id" = ?;', (json_data['name'], id,)) or abort(404, detail='Platform not found')
    query_db('COMMIT;')
    return '', 204


@platform.delete('/<int:id>')
@platform.auth_required(auth)
@platform.doc(description='Delete a platform', responses=[204])
@platform.input(AuthorizationHeader, location='headers')
@platform.output(EmptySchema, 204)
def delete_platform(id):
    query_db('DELETE FROM "platforms" WHERE "id" = ?;', (id,))
    query_db('COMMIT;')
    return '', 204
    