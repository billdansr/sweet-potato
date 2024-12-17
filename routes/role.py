from apiflask import APIBlueprint, abort
from db import query_db
from flask import url_for
from routes import auth
from schemas import RoleIn, RoleOut, RolesOut, EmptySchema, CreatedSchema, AuthorizationHeader

role = APIBlueprint('role', __name__)


@role.post('/')
@role.auth_required(auth, roles=['admin'])
@role.doc(description='Create a role', responses=[201,  409])
@role.input(AuthorizationHeader, location='headers')
@role.input(RoleIn, location='json', example=RoleIn.example())
@role.output(CreatedSchema, 201, example=CreatedSchema.example())
def create_role(json_data):
    role_id = query_db('INSERT INTO "roles" ("name") VALUES (?);', (json_data['name'],)) if not query_db('SELECT "name" FROM "roles" WHERE "name" = ? LIMIT 1;', (json_data['name'],), one=True) else abort(409, detail={"field": "name", "issue": f"Role already exists: {json_data['name']}"})
    query_db('COMMIT;')
    return {'message': 'Role created successfully!', 'id': role_id}, 201


@role.get('/')
@role.doc(description='List roles', responses=[200, 404])
@role.output(RolesOut(many=True), 200, example=RolesOut.example())
def read_roles():
    print('h')
    results = [dict(result) for result in query_db('SELECT * FROM "roles"')] or abort(404, detail='Roles not found')

    for result in results:
        result['url'] = url_for('role.read_role', id=result['id'], _external=True)
        del result['id']
    
    return results, 200


@role.get('/<int:id>')
@role.doc(description='Single role', responses=[200,  404])
@role.output(RoleOut, 200, example=RoleOut.example())
def read_role(id):
    result = dict(query_db('SELECT * FROM "roles" WHERE "id" = ?', (id,), one=True) or abort(404, detail='Role not found'))
    return result, 200


@role.patch('/<int:id>')
@role.auth_required(auth, roles=['admin'])
@role.doc(description='Update a role', responses=[204,  404])
@role.input(AuthorizationHeader, location='headers')
@role.input(RoleIn, location='json', example=RoleIn.example())
@role.output(EmptySchema, 204)
def update_role(id, json_data):
    query_db('UPDATE "roles" SET "name" = ? WHERE "id" = ?;', (json_data['name'], id,)) or abort(404, detail='Role not found')
    query_db('COMMIT;')
    return '', 204


@role.delete('/<int:id>')
@role.auth_required(auth, roles=['admin'])
@role.doc(description='Delete a role', responses=[204])
@role.input(AuthorizationHeader, location='headers')
@role.output(EmptySchema, 204)
def delete_role(id):
    query_db('DELETE FROM "roles" WHERE "id" = ?;', (id,))
    query_db('COMMIT;')
    return '', 204
