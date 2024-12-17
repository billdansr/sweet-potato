from apiflask import APIBlueprint, abort
from db import query_db
from flask import url_for
from routes import auth
from schemas import CompanyIn, CompanyOut, CompaniesOut, EmptySchema, CreatedSchema, AuthorizationHeader

company = APIBlueprint('company', __name__)


@company.post('/')
@company.auth_required(auth, roles=['admin'])
@company.doc(description='Create a company', responses=[201, 409])
@company.input(AuthorizationHeader, location='headers')
@company.input(CompanyIn, location='json', example=CompanyIn.example())
@company.output(CreatedSchema, 201, example=CreatedSchema.example())
def create_company(json_data):
    company_id = query_db('INSERT INTO "companies" ("name") VALUES (?);', (json_data['name'],)) if not query_db('SELECT "name" FROM "companies" WHERE "name" = ? LIMIT 1;', (json_data['name'],), one=True) else abort(409, detail={"field": "name", "issue": f"Company already exists: {json_data['name']}"})
    query_db('COMMIT;')
    return {'message': 'Company created successfully!', 'id': company_id}, 201


@company.get('/')
@company.doc(description='Retrieve list companies', responses=[200, 404])
@company.output(CompaniesOut(many=True), 200, example=CompaniesOut.example())
def read_companies():
    results = [dict(result) for result in query_db('SELECT "name", "id" FROM "companies";')] or abort(404, detail='Companies not found')

    for result in results:
        result['url'] = url_for('company.read_company', id=result['id'], _external=True)
        del result['id']
    print(results)
        
    return results, 200


@company.get('/<int:id>')
@company.doc(description='Single company', responses=[200, 404])
@company.output(CompanyOut, 200, example=CompanyOut.example())
def read_company(id):
    result = dict(query_db('SELECT "id", "name", "founding_date" FROM "companies" WHERE "id" = ?;', (id,), one=True) or abort(404, detail='Company not found'))

    headquarters = []
    for location in query_db('SELECT "location" FROM "view_company_headquarters" WHERE "company_id" = ?;', (id,)):
        headquarters.append(location['location'])
    
    roles = [dict(role) for role in query_db('SELECT "role_id", "role" AS "name" FROM "view_company_roles" WHERE "company_id" = ?;', (id,))]
    for role in roles:
        role['url'] = url_for('role.read_role', id=role['role_id'], _external=True)
        del role['role_id']
    
    result['headquarters'] = headquarters
    result['roles'] = roles

    return result, 200


@company.patch('/<int:id>')
@company.auth_required(auth, roles=['admin'])
@company.doc(description='Update a company', responses=[204, 404])
@company.input(AuthorizationHeader, location='headers')
@company.input(CompanyIn, location='json', example=CompanyIn.example())
@company.output(EmptySchema, 204)
def update_company(id, json_data):
    name = json_data['name']
    founding_date = json_data['founding_date']
    headquarters = json_data['headquarters']
    roles =  json_data['roles']

    if name:
        query_db('UPDATE "companies" SET "name" = ? WHERE "id" = ?;', (name, id,)) or abort(404, detail='Company not found')
    if founding_date:
        query_db('UPDATE "companies" SET "founding_date" = unixepoch(?) WHERE "id" = ?;', (founding_date, id,))
    if headquarters:
        query_db('DELETE FROM "headquarters" WHERE "company_id" = ?;', (id,))
        for location in headquarters:
            query_db('INSERT INTO "headquarters" ("location", "company_id") VALUES (?, ?);', (location, id,))
    if roles:
        query_db('DELETE FROM "company_roles" WHERE "company_id" = ?;', (id,))
        for role in roles:
            query_db('INSERT INTO "company_roles" ("company_id", "role_id") VALUES (?, ?);', (id, role,))

    query_db('COMMIT;')

    return '', 204


@company.delete('/<int:id>')
@company.auth_required(auth, roles=['admin'])
@company.doc(description='Delete a company', responses=[204])
@company.input(AuthorizationHeader, location='headers')
@company.output(EmptySchema, 204)
def delete_company(id):
    query_db('DELETE FROM "companies" WHERE "id" = ?;', (id,))
    query_db('COMMIT;')
    return '', 204
