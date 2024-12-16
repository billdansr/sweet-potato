from apiflask import APIBlueprint, abort
from db import query_db
from flask import url_for
from schemas import CompanyIn, CompanyOut, CompaniesOut, EmptySchema

company = APIBlueprint('company', __name__, url_prefix='/api/companies')


@company.post('/')
@company.doc(description='Create a company', responses=[201, 409])
@company.input(CompanyIn, location='json', example=CompanyIn.example())
def create_company(json_data):
    company_id = query_db('INSERT INTO "companies" ("name") VALUES (?);', (json_data['name'],)) if not query_db('SELECT "name" FROM "companies" WHERE "name" = ? LIMIT 1;', (json_data['name'],), one=True) else abort(409, detail={"field": "name", "issue": f"Company already exists: {json_data['name']}"})
    query_db('COMMIT;')
    return {'message': 'Company created successfully!', 'id': company_id}, 201


@company.get('/')
@company.doc(description='Retrieve list companies', responses=[200, 404])
@company.output(CompaniesOut(many=True), example=CompaniesOut.example())
def read_companies():
    results = [dict(result) for result in query_db('SELECT "name", "id" FROM "companies"')] or abort(404, detail='Companies not found')
    print(results)
    for result in results:
        result['url'] = url_for('company.read_company', id=result['id'], _external=True)
        del result['id']
    print(results)
        
    return results, 200


@company.get('/<int:id>')
@company.doc(description='Single company', responses=[200, 404])
@company.output(CompanyOut, example=CompanyOut.example())
def read_company(id):
    result = dict(query_db('SELECT * FROM "companies" WHERE "id" = ?', (id,), one=True)) or abort(404, detail='Company not found')

    headquarters = [dict(headquarter) for headquarter in query_db('''SELECT "headquarters"."location"
                                                                FROM "headquarters"
                                                                LEFT JOIN "companies"
                                                                ON "companies"."id" = "headquarters"."company_id"
                                                                WHERE "companies"."id" = ?''', 
                                                                (id,))]
    
    roles = [dict(role) for role in query_db('''SELECT "roles"."name", "roles"."id" 
                                            FROM "roles"
                                            INNER JOIN "company_roles"
                                            ON "roles"."id" = "company_roles"."role_id"
                                            WHERE "company_roles"."company_id" = ?''', (id,))]
    for role in roles:
        role['url'] = url_for('role.read_role', id=role['id'], _external=True)
        del role['id']
    
    result['headquarters'] = headquarters
    result['roles'] = roles

    return result, 200


@company.patch('/<int:id>')
@company.doc(description='Update a company', responses=[204, 404])
@company.input(CompanyIn, location='json', example=CompanyIn.example())
@company.output(EmptySchema, status_code=204)
def update_company(id, json_data):
    name = json_data['name']
    founding_date = json_data['founding_date']
    headquarters = json_data['headquarters']
    roles =  json_data['roles']

    if name:
        query_db('UPDATE "companies" SET "name" = ? WHERE "id" = ?;', (name, id,)) or abort(404, detail='Company not found')
    if founding_date:
        query_db('UPDATE "companies" SET "founding_date" = UNIXEPOCH(?) WHERE "id" = ?;', (founding_date, id,))
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
@company.doc(description='Delete a company', responses=[204])
@company.output(EmptySchema, status_code=204)
def delete_company(id):
    query_db('DELETE FROM "companies" WHERE "id" = ?;', (id,))
    query_db('COMMIT;')
    return '', 204
