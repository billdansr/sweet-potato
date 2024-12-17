import os
from apiflask import APIBlueprint, abort
from routes import auth
from datetime import datetime, timezone
from db import query_db
from flask import url_for, current_app
from schemas import GameIn, GameOut, GamesOut, GamesQuery, EmptySchema, CreatedSchema, AuthorizationHeader
from werkzeug.utils import secure_filename

game = APIBlueprint('game', __name__)


@game.post('/')
@game.auth_required(auth, roles=['admin'])
@game.doc(description='Create a new game', responses=[201, 409, 422])
@game.input(AuthorizationHeader, location='headers')
@game.input(GameIn, location='files')
@game.output(CreatedSchema, 201, example=CreatedSchema.example())
def create_game(files_data):
    title = files_data.get('title')
    description = files_data.get('description')
    release_date = files_data.get('release_date')
    genres = files_data.get('genres')
    platforms = files_data.get('platforms')
    companies = files_data.get('companies')
    media = files_data.get('media')

    game_id = query_db('INSERT INTO "games" ("title", "description", "release_date") VALUES (?, ?, strftime(\'%s\', ?));', 
            (title, description, release_date,)) if not query_db('SELECT "title" FROM "games" WHERE "title" = ? LIMIT 1;', (title,), one=True) else abort(409, detail={"field": "title", "issue": f"Game title already exists: {title}"})
    
    if genres:
        for genre in genres:
            if genre.strip():
                query_db('INSERT INTO "game_genres" ("game_id", "genre_id") VALUES (?, (SELECT "id" FROM "genres" WHERE "name" = ? LIMIT 1));', 
                        (game_id, genre,)) if query_db('SELECT "name" FROM "genres" WHERE "name" = ? LIMIT 1;', (genre,), one=True) else abort(422, detail={"field": "genres", "issue": f"Genre does not exists: {genre}"})
            else: abort(422, detail={"field": "genres", "issue": f"Value is not valid: {genre}"})
        
    if platforms:
        for platform in platforms:
            if platform.strip():
                query_db('INSERT INTO "game_platforms" ("game_id", "platform_id")  VALUES (?, (SELECT "id" FROM "platforms" WHERE "name" = ? LIMIT 1));',
                        (game_id, platform,)) if query_db('SELECT "name" FROM "platforms" WHERE "name" = ? LIMIT 1;', (platform,), one=True) else abort(422, detail={"field": "platforms", "issue": f"Platform does not exists: {platform}"})
            else: abort(422, detail={"field": "platforms", "issue": f"Value is not valid: {platform}"})
        
    if companies:
        for company in companies:
            if company.strip():
                query_db('INSERT INTO "game_companies" ("game_id", "company_id")  VALUES (?, (SELECT "id" FROM "companies" WHERE "name" = ? LIMIT 1));',
                        (game_id, company,)) if query_db('SELECT "name" FROM "companies" WHERE "name" = ? LIMIT 1;', (company,), one=True) else abort(422, detail={"field": "companies", "issue": f"Company does not exists: {company}"})
            else: abort(422, detail={"field": "companies", "issue": f"Value is not valid: {company}"})

    if media:        
        for media_file in media:
                filename = secure_filename(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z') + '_' + media_file.filename)
                media_file.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
                query_db('INSERT INTO "media" ("game_id", "filename") VALUES (?, ?);',
                            (game_id, filename,))
            
    query_db('COMMIT;')
        
    return {'message': 'Game is added successfully!', 'id': game_id}, 201


@game.get('/')
@game.doc(description='List of games', responses=[200, 404])
@game.input(GamesQuery, location='query')
@game.output(GamesOut, 200, example=GamesOut.example())
def read_games(query_data):
    offset = query_data.get('offset')
    limit = query_data.get('limit')

    count = query_db('SELECT COUNT(*) FROM "games";', one=True)['COUNT(*)']

    next = url_for('game.read_games', offset=offset + limit, limit=limit, _external=True) if offset + limit < count else None
    previous = url_for('game.read_games', offset=offset - limit, limit=limit, _external=True) if  offset - limit >= 0 else None

    results = [dict(result) for result in query_db('SELECT "id", "title" FROM "games" LIMIT ? OFFSET ?;', (limit, offset,))] or abort(404, detail="No games found")

    for game in results:
        game['url'] = url_for('game.read_game', id=game['id'], _external=True)
        del game['id']

    return {
    'count': count,
    'next': next,
    'previous': previous,
    'results': results,
}, 200


@game.get('/<int:id>')
@game.doc(description='Single game', responses=[200, 404])
@game.output(GameOut, 200, example=GameOut.example())
def read_game(id):
    result = dict(query_db('SELECT "id", "title", "description", "release_date" FROM "games" WHERE "id" = ?;', 
                (id,), one=True) or abort(404, detail='Game not found'))
    
    genres = [dict(genre) for genre in query_db('SELECT "genre" AS "name", "genre_id" FROM "view_game_genres" WHERE "game_id" = ?;', (id,))]
    for genre in genres:
        genre['url'] = url_for('genre.read_genre', id=genre['genre_id'], _external=True)
        del genre['genre_id']

    platforms = [dict(platform) for platform in query_db('SELECT "platform" AS "name" , "platform_id" FROM "view_game_platforms" WHERE "game_id" = ?;', (id,))]
    for platform in platforms:
        platform['url'] = url_for('platform.read_platform', id=platform['platform_id'], _external=True)
        del platform['platform_id']

    companies = [dict(company) for company in query_db('SELECT "company" AS "name" , "company_id" FROM "view_game_companies" WHERE "game_id" = ?;', (id,))]
    for company in companies:
        company['url'] = url_for('company.read_company', id=company['company_id'], _external=True)
        del company['company_id']

    result['release_date'] = datetime.fromtimestamp(result['release_date'], timezone.utc) if result['release_date'] else None
    result['genres'] = genres
    result['platforms'] = platforms
    result['companies'] = companies
    result['media'] = url_for('game.read_game_media', id=id, _external=True)

    return result, 200


@game.patch('/<int:id>')
@game.auth_required(auth, roles=['admin'])
@game.doc(description='Update a game', responses=[204, 404, 422])
@game.input(AuthorizationHeader, location='headers')
@game.input(GameIn, location='files')
@game.output(EmptySchema, 204)
def update_game(id, files_data):
    title = files_data.get('title')
    description = files_data.get('description')
    release_date = files_data.get('release_date')
    genres = files_data.get('genres')
    platforms = files_data.get('platforms')
    companies = files_data.get('companies')
    media = files_data.get('media')

    if title:
        query_db('UPDATE "games" SET "title" = ? WHERE "id" = ?;', (title, id,)) or abort(404, detail='Game not found')
    if description:
        query_db('UPDATE "games" SET "description" = ? WHERE "id" = ?;', (description, id,))
    if release_date:
        query_db('UPDATE "games" SET "release_date" = strftime(\'%s\', ?) WHERE "id" = ?;', (release_date, id,))
    if genres:
        query_db('DELETE FROM "game_genres" WHERE "game_id" = ?;', (id,))
        for genre in genres:
            if genre.strip():
                query_db('INSERT INTO "game_genres" ("game_id", "genre_id") VALUES (?, (SELECT "id" FROM "genres" WHERE "name" = ?));',
                            (id, genre,)) if query_db('SELECT "name" FROM "genres" WHERE "name" = ?;', (genre,), one=True) else abort(422, detail={"field": "genres", "issue": f"Genre does not exists: {genre}"})
            else: abort(422, detail={"field": "genres", "issue": f"Value is not valid: {genre}"})
    if platforms:
        query_db('DELETE FROM "game_platforms" WHERE "game_id" = ?;', (id,))
        for platform in platforms:
            if platform.strip():
                query_db('INSERT INTO "game_platforms" ("game_id", "platform_id") VALUES (?, (SELECT "id" FROM "platforms" WHERE "name" = ?));',
                            (id, platform,)) if query_db('SELECT "name" FROM "platforms" WHERE "name" = ?;', (platform,), one=True) else abort(422, detail={"field": "platforms", "issue": f"Platform does not exists: {platform}"})
            else: abort(422, detail={"field": "platforms", "issue": f"Value is not valid: {platform}"})
    if companies:
        query_db('DELETE FROM "game_companies" WHERE "game_id" = ?;', (id,))
        for company in companies:
            if company.strip():
                query_db('INSERT INTO "game_companies" ("game_id", "company_id") VALUES (?, (SELECT "id" FROM "companies" WHERE "name" = ?));', 
                            (id, company,)) if query_db('SELECT "name" FROM "companies" WHERE "name" = ?;', (company,), one=True) else abort(422, detail={"field": "companies", "issue": f"Company does not exists: {company}"})
            else: abort(422, detail={"field": "companies", "issue": f"Value is not valid: {company}"})
    if media:
        query_db('DELETE FROM "media" WHERE "game_id" = ?;', (id,))
        for media_file in media:
            query_db('INSERT INTO "media" ("game_id", "filename") VALUES (?, ?);', (id, media_file,))
    
    query_db('COMMIT;')

    return '', 204


@game.delete('/<int:id>')
@game.auth_required(auth, roles=['admin'])
@game.doc(description='Delete a game', responses=[204])
@game.input(AuthorizationHeader, location='headers')
@game.output(EmptySchema, 204)
def delete_game(id):
    for filename in query_db('SELECT "filename" FROM "media" WHERE "game_id" = ?;', (id,)):
        file_path = os.path.join(current_app.config['UPLOAD_DIR'], filename['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)

    query_db('DELETE FROM "games" WHERE "id" = ?;', (id,))
    query_db('COMMIT;')

    return '', 204

@game.get('/<int:id>/media')
@game.doc(description='Retrieve a game\'s media', responses=[200, 404])
def read_game_media(id):
    media = query_db('SELECT "filename" FROM "media" WHERE "game_id" = ?;', (id,)) or abort(404, detail='Game not found')
    return [url_for('read_upload', filename=media_file['filename'], _external=True) for media_file in media], 200
