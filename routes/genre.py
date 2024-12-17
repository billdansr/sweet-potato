from apiflask import APIBlueprint, abort
from db import query_db
from flask import url_for
from routes import auth
from schemas import GenreIn, GenreOut, GenresOut, EmptySchema, CreatedSchema, AuthorizationHeader

genre = APIBlueprint('genre', __name__)


@genre.post('/')
@genre.auth_required(auth, roles=['admin'])
@genre.doc(description='Create a genre', responses=[201, 409])
@genre.input(AuthorizationHeader, location='headers')
@genre.input(GenreIn, location='json', example=GenreIn.example())
@genre.output(CreatedSchema, 201, example=CreatedSchema.example())
def create_genre(json_data, headers_data):
    genre_id = query_db('INSERT INTO "genres" ("name") VALUES (?);', (json_data['name'],)) if not query_db('SELECT "name" FROM "genres" WHERE "name" = ? LIMIT 1;', (json_data['name'],), one=True) else abort(409, detail={"field": "name", "issue": f"Genre already exists: {json_data['name']}"})
    query_db('COMMIT;')
    return {'message': 'Genre created successfully!', 'id': genre_id}, 201


@genre.get('/')
@genre.doc(description='Retrieve list genres', responses=[200, 404])
@genre.output(GenresOut(many=True), 200, example=GenresOut.example())
def read_genres():
    results = [dict(result) for result in query_db('SELECT * FROM "genres";')] or abort(404, detail='Genres not found')
    for result in results:
        result['url'] = url_for('genre.read_genre', id=result['id'], _external=True)
        del result['id']

    return results, 200


@genre.get('/<int:id>')
@genre.doc(description='Single genre', responses=[200, 404])
@genre.output(GenreOut, 200, example=GenreOut.example())
def read_genre(id):
    result = dict(query_db('SELECT * FROM "genres" WHERE "id" = ?;', (id,), one=True) or abort(404, detail='Genre not found'))
    return result, 200


@genre.patch('/<int:id>')
@genre.auth_required(auth, roles=['admin'])
@genre.doc(description='Update a genre', responses=[204, 404])
@genre.input(AuthorizationHeader, location='headers')
@genre.input(GenreIn, location='json', example=GenreIn.example())
@genre.output(EmptySchema, 204)
def update_genre(id, json_data, headers_data):
    query_db('UPDATE "genres" SET "name" = ? WHERE "id" = ?;', (json_data['name'], id,)) or abort(404, detail='Genre not found')
    return '', 204


@genre.delete('/<int:id>')
@genre.auth_required(auth, roles=['admin'])
@genre.doc(description='Delete a genre', responses=[204])
@genre.input(AuthorizationHeader, location='headers')
@genre.output(EmptySchema, 204)
def delete_genre(id, headers_data):
    query_db('DELETE FROM "genres" WHERE "id" = ?;', (id,))
    query_db('COMMIT;')
    return '', 204
