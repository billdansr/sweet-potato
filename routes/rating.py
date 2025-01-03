from apiflask import APIBlueprint, abort
from datetime import datetime, timezone
from db import query_db
from routes import auth
from schemas import RatingIn, RatingOut, CreatedSchema, UpdatedSchema, AuthorizationHeader, EmptySchema

rating = APIBlueprint('rating', __name__)


@rating.post('')
@rating.auth_required(auth)
@rating.doc(description='Create rating', responses=[201, 404, 409])
@rating.input(AuthorizationHeader, location='headers')
@rating.input(RatingIn, location='json', example=RatingIn.example())
@rating.output(CreatedSchema, 201, example=CreatedSchema.example())
def create_rating(json_data, headers_data):
    user = auth.current_user
    game_id = json_data.get('game_id')
    score = json_data.get('score')
    review = json_data.get('review')

    if query_db('SELECT * FROM "ratings" WHERE "user_id" = ? AND "game_id" = ?;', (user['id'], game_id), one=True):
        abort(409, detail='You have already rated this game.')

    if not query_db('SELECT * FROM "games" WHERE "id" = ?;', (game_id,), one=True):
        abort(404, detail='Game not found.')

    rating_id = query_db('INSERT INTO "ratings" ("user_id", "game_id", "score", "review") VALUES (?, ?, ?, ?);', 
                            (user['id'], game_id, score, review))
    
    query_db('COMMIT;')
    
    return {'message': 'Rating added successfully!', 'id': rating_id}, 201


@rating.get('/')
@rating.doc(description='List ratings', responses=[200, 404])
@rating.output(RatingOut(many=True), 200, example=RatingOut.example())
def get_ratings():
    results = [dict(result) for result in query_db('SELECT "game", "user", "avatar", "score", "review", "created_at", "updated_at" FROM "view_game_ratings";') or abort(404, detail='No ratings found.')]

    for result in results:
        result['created_at'] = datetime.fromtimestamp(result['created_at'], timezone.utc) if result['created_at'] else None
        result['updated_at'] = datetime.fromtimestamp(result['updated_at'], timezone.utc) if result['updated_at'] else None

    return results, 200


@rating.patch('/<int:id>')
@rating.auth_required(auth)
@rating.doc(description='Update rating', responses=[200, 404])
@rating.input(AuthorizationHeader, location='headers')
@rating.input(RatingIn, location='json', example=RatingIn.example())
@rating.output(UpdatedSchema, 200, example=UpdatedSchema.example())
def update_rating(id, json_data, headers_data):
    user = auth.current_user
    score = json_data.get('score')
    review = json_data.get('review')

    if not query_db('SELECT * FROM "ratings" WHERE "user_id" = ? AND "game_id" = ?;', (user['id'], id,), one=True):
        abort(404, detail='Rating not found.')

    query_db('UPDATE "ratings" SET "score" = ?, "review" = ? WHERE "user_id" = ? AND "game_id" = ?;', (score, review, user['id'], id,))
    query_db('COMMIT;')

    return {'message': 'Rating updated successfully!'}, 200


@rating.delete('/<int:id>')
@rating.auth_required(auth)
@rating.doc(description='Delete rating', responses=[204])
@rating.input(AuthorizationHeader, location='headers')
@rating.output(EmptySchema, 204)
def delete_rating(id, headers_data):
    query_db('DELETE FROM "ratings" WHERE "user_id" = ? AND "game_id" = ?;', 
                (auth.current_user['id'], id,))
    query_db('COMMIT;')
    return '', 204
