import os
from apiflask import abort
from apiflask.schemas import EmptySchema
from datetime import datetime, timezone
from db import query_db
from flask import url_for, request, send_from_directory
from schemas import *
from werkzeug.utils import secure_filename
    

def init_game_routes(app, auth):
    @app.post('/api/games')
    @app.doc(description='Create a new game', responses=[201, 409, 422])
    @app.input(GameIn, location='files')
    def create_game(files_data):
        title = files_data.get('title')
        description = files_data.get('description')
        release_date = files_data.get('release_date')
        genres = files_data.get('genres')
        platforms = files_data.get('platforms')
        companies = files_data.get('companies')
        media = files_data.get('media')

        game_id = query_db('INSERT INTO "games" ("title", "description", "release_date") VALUES (?, ?, UNIXEPOCH(?));', 
                (title, description, release_date,)) if not query_db('SELECT "title" FROM "games" WHERE "title" = ? LIMIT 1;', (title,), one=True) else abort(409, detail={"field": "title", "issue": f"Game title already exists: {title}"})
        
        for genre in genres:
            if genre.strip():
                query_db('INSERT INTO "game_genres" ("game_id", "genre_id") VALUES (?, (SELECT "id" FROM "genres" WHERE "name" = ? LIMIT 1));', 
                        (game_id, genre,)) if query_db('SELECT "name" FROM "genres" WHERE "name" = ? LIMIT 1;', (genre,), one=True) else abort(422, detail={"field": "genres", "issue": f"Genre does not exists: {genre}"})
            else: abort(422, detail={"field": "genres", "issue": f"Value is not valid: {genre}"})
            
        for platform in platforms:
            if platform.strip():
                query_db('INSERT INTO "game_platforms" ("game_id", "platform_id")  VALUES (?, (SELECT "id" FROM "platforms" WHERE "name" = ? LIMIT 1));',
                        (game_id, platform,)) if query_db('SELECT "name" FROM "platforms" WHERE "name" = ? LIMIT 1;', (platform,), one=True) else abort(422, detail={"field": "platforms", "issue": f"Platform does not exists: {platform}"})
            else: abort(422, detail={"field": "platforms", "issue": f"Value is not valid: {platform}"})
            
        for company in companies:
            if company.strip():
                query_db('INSERT INTO "game_companies" ("game_id", "company_id")  VALUES (?, (SELECT "id" FROM "companies" WHERE "name" = ? LIMIT 1));',
                        (game_id, company,)) if query_db('SELECT "name" FROM "companies" WHERE "name" = ? LIMIT 1;', (company,), one=True) else abort(422, detail={"field": "companies", "issue": f"Company does not exists: {company}"})
            else: abort(422, detail={"field": "companies", "issue": f"Value is not valid: {company}"})
            
        for media_file in media:
                filename = secure_filename(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z') + '_' + media_file.filename)
                media_file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
                query_db('INSERT INTO "media" ("game_id", "filename") VALUES (?, ?);',
                            (game_id, filename,))
                
        query_db('COMMIT;')
            
        return {'message': 'Game is added successfully!', 'id': game_id}, 201

    @app.get('/api/games')
    @app.doc(description='List games', responses=[200, 404])
    @app.output(GamesOut, example=GamesOut.example())
    def read_games():
        offset = request.args.get('offset', type=int, default=0)
        limit = request.args.get('limit', type=int, default=20)

        results = query_db('SELECT "id", "title" FROM "games" LIMIT ? OFFSET ?;', (limit, offset,)) or abort(404, detail="No games found")

        count = query_db('SELECT COUNT(*) FROM "games";', one=True)['COUNT(*)']

        next = url_for('read_games', offset=offset + limit, limit=limit, _external=True) if offset + limit < count else None
        
        previous = url_for('read_games', offset=offset - limit, limit=limit, _external=True) if  offset - limit >= 0 else None
        
        results = [dict(result) for result in results]
        
        for game in results:
            game['url'] = url_for('read_game', id=game['id'], _external=True)
            del game['id']
        
        return {
            'count': count,
            'next': next,
            'previous': previous,
            'results': results,
        }, 200

    @app.get('/api/games/<int:id>')
    @app.doc(description='Single game', responses=[200, 404])
    @app.output(GameOut, example=GameOut.example())
    def read_game(id):
        result = dict(query_db('SELECT "id", "title", "description", "release_date" FROM "games" WHERE "id" = ?;', 
                    (id,), one=True) or abort(404, detail='Game not found'))
        
        genres = [dict(genre) for genre in query_db('''SELECT "genres"."name" , "genres"."id"
                                                    FROM "genres"
                                                    INNER JOIN "game_genres" 
                                                    ON "game_genres"."genre_id" = "genres"."id"
                                                    WHERE "game_genres"."game_id" = ?;''', 
                                                    (id,), one=False)]
        for genre in genres:
            genre['url'] = url_for('read_genre', id=genre['id'], _external=True)
            del genre['id']

        platforms = [dict(platform) for platform in query_db('''SELECT "platforms"."name" , "platforms"."id"
                                                            FROM "platforms"
                                                            INNER JOIN "game_platforms"
                                                            ON "game_platforms"."platform_id" = "platforms"."id"
                                                            WHERE "game_platforms"."game_id" = ?;''',
                                                            (id,), one=False)]
        for platform in platforms:
            platform['url'] = url_for('read_platform', id=platform['id'], _external=True)
            del platform['id']

        companies = [dict(company) for company in query_db('''SELECT "companies"."name" , "companies"."id"
                                                        FROM "companies"
                                                        INNER JOIN "game_companies"
                                                        ON "game_companies"."company_id" = "companies"."id"
                                                        WHERE "game_companies"."game_id" = ?;''',
                                                        (id,), one=False)]
        for company in companies:
            company['url'] = url_for('read_company', id=company['id'], _external=True)
            del company['id']

        result['release_date'] = datetime.fromtimestamp(result['release_date'], tz=timezone.utc)
        result['genres'] = genres
        result['platforms'] = platforms
        result['companies'] = companies
        result['media'] = url_for('read_game_media', id=id, _external=True)

        return result, 200
    
    @app.patch('/api/games/<int:id>')
    @app.doc(description='Update a game', responses=[204, 404, 422])
    @app.input(GameIn, location='files')
    @app.output(EmptySchema, status_code=204)
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
            query_db('UPDATE "games" SET "release_date" = UNIXEPOCH(?) WHERE "id" = ?;', (release_date, id,))
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

    @app.delete('/api/games/<int:id>')
    @app.doc(description='Delete a game', responses=[204])
    @app.output(EmptySchema, status_code=204)
    def delete_game(id):
        query_db('DELETE FROM "games" WHERE "id" = ?;', (id,))
        query_db('COMMIT;')
        return '', 204

    @app.get('/api/games/<int:id>/media')
    @app.doc(description='Retrieve a game\'s media', responses=[200, 404])
    def read_game_media(id):
        media = query_db('SELECT "filename" FROM "media" WHERE "game_id" = ?;', (id,)) or abort(404, detail='Game not found')
        return [url_for('read_upload', filename=media_file['filename'], _external=True) for media_file in media], 200


def init_genre_routes(app):
    @app.post('/api/genres')
    @app.doc(description='Create a genre', responses=[201, 409])
    @app.input(GenreIn, location='json', example=GenreIn.example())
    def create_genre(json_data):
        genre_id = query_db('INSERT INTO "genres" ("name") VALUES (?);', (json_data['name'],)) if not query_db('SELECT "name" FROM "genres" WHERE "name" = ? LIMIT 1;', (json_data['name'],), one=True) else abort(409, detail={"field": "name", "issue": f"Genre already exists: {json_data['name']}"})
        query_db('COMMIT;')
        return {'message': 'Genre created successfully!', 'id': genre_id}, 201

    @app.get('/api/genres')
    @app.doc(description='Retrieve list genres', responses=[200, 404])
    @app.output(GenresOut(many=True), example=GenresOut.example())
    def read_genres():
        results = [dict(result) for result in query_db('SELECT * FROM "genres";')] or abort(404, detail='Genres not found')
        for result in results:
            result['url'] = url_for('read_genre', id=result['id'], _external=True)
            del result['id']

        return results, 200
    
    @app.get('/api/genres/<int:id>')
    @app.doc(description='Single genre', responses=[200, 404])
    @app.output(GenreOut, example=GenreOut.example())
    def read_genre(id):
        result = dict(query_db('SELECT * FROM "genres" WHERE "id" = ?;', (id,), one=True)) or abort(404, detail='Genre not found')
        return result, 200
    
    @app.patch('/api/genres/<int:id>')
    @app.doc(description='Update a genre', responses=[204, 404])
    @app.input(GenreIn, location='json', example=GenreIn.example())
    @app.output(EmptySchema, status_code=204)
    def update_genre(id, json_data):
        query_db('UPDATE "genres" SET "name" = ? WHERE "id" = ?;', (json_data['name'], id,)) or abort(404, detail='Genre not found')
        return '', 204

    @app.delete('/api/genres/<int:id>')
    @app.doc(description='Delete a genre', responses=[204])
    @app.output(EmptySchema, status_code=204)
    def delete_genre(id):
        query_db('DELETE FROM "genres" WHERE "id" = ?;', (id,))
        query_db('COMMIT;')
        return '', 204
    

def init_platform_routes(app):
    @app.post('/api/platforms')
    @app.doc(description='Create a platform', responses=[201, 409])
    @app.input(PlatformIn, location='json', example=PlatformIn.example())
    def create_platform(json_data):
        platform_id = query_db('INSERT INTO "platforms" ("name") VALUES (?);', (json_data['name'],)) if not query_db('SELECT "name" FROM "platforms" WHERE "name" = ? LIMIT 1;', (json_data['name'],), one=True) else abort(409, detail={"field": "name", "issue": f"Platform already exists: {json_data['name']}"})
        query_db('COMMIT;')
        return {'message': 'Platform created successfully!', 'id': platform_id}, 201

    @app.get('/api/platforms')
    @app.doc(description='Retrieve list platforms', responses=[200, 404])
    @app.output(PlatformsOut(many=True), example=PlatformsOut.example())
    def read_platforms():
        results = [dict(result) for result in query_db('SELECT * FROM "platforms"')] or abort(404, detail='Platforms not found')

        for result in results:
            result['url'] = url_for('read_platform', id=result['id'], _external=True)
            del result['id']
        
        return results, 200
    
    @app.get('/api/platforms/<int:id>')
    @app.doc(description='Single platform', responses=[200, 404])
    @app.output(PlatformOut, example=PlatformOut.example())
    def read_platform(id):
        result = dict(query_db('SELECT * FROM "platforms" WHERE "id" = ?', (id,), one=True)) or abort(404, detail='Platform not found')
        return result, 200
    
    @app.patch('/api/platforms/<int:id>')
    @app.doc(description='Update a platform', responses=[204, 404])
    @app.input(PlatformIn, location='json', example=PlatformIn.example())
    @app.output(EmptySchema, status_code=204)
    def update_platform(id, json_data):
        query_db('UPDATE "platforms" SET "name" = ? WHERE "id" = ?;', (json_data['name'], id,)) or abort(404, detail='Platform not found')
        query_db('COMMIT;')
        return '', 204

    @app.delete('/api/platforms/<int:id>')
    @app.doc(description='Delete a platform', responses=[204])
    @app.output(EmptySchema, status_code=204)
    def delete_platform(id):
        query_db('DELETE FROM "platforms" WHERE "id" = ?;', (id,))
        query_db('COMMIT;')
        return '', 204
    

def init_company_routes(app):
    @app.post('/api/companies')
    @app.doc(description='Create a company', responses=[201, 409])
    @app.input(CompanyIn, location='json', example=CompanyIn.example())
    def create_company(json_data):
        company_id = query_db('INSERT INTO "companies" ("name") VALUES (?);', (json_data['name'],)) if not query_db('SELECT "name" FROM "companies" WHERE "name" = ? LIMIT 1;', (json_data['name'],), one=True) else abort(409, detail={"field": "name", "issue": f"Company already exists: {json_data['name']}"})
        query_db('COMMIT;')
        return {'message': 'Company created successfully!', 'id': company_id}, 201

    @app.get('/api/companies')
    @app.doc(description='Retrieve list companies', responses=[200, 404])
    @app.output(CompaniesOut(many=True), example=CompaniesOut.example())
    def read_companies():
        results = [dict(result) for result in query_db('SELECT "name", "id" FROM "companies"')] or abort(404, detail='Companies not found')
        print(results)
        for result in results:
            result['url'] = url_for('read_company', id=result['id'], _external=True)
            del result['id']
        print(results)
            
        return results, 200
    
    @app.get('/api/companies/<int:id>')
    @app.doc(description='Single company', responses=[200, 404])
    @app.output(CompanyOut, example=CompanyOut.example())
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
            role['url'] = url_for('read_role', id=role['id'], _external=True)
            del role['id']
        
        result['headquarters'] = headquarters
        result['roles'] = roles

        return result, 200
    
    @app.patch('/api/companies/<int:id>')
    @app.doc(description='Update a company', responses=[204, 404])
    @app.input(CompanyIn, location='json', example=CompanyIn.example())
    @app.output(EmptySchema, status_code=204)
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

    @app.delete('/api/companies/<int:id>')
    @app.doc(description='Delete a company', responses=[204])
    @app.output(EmptySchema, status_code=204)
    def delete_company(id):
        query_db('DELETE FROM "companies" WHERE "id" = ?;', (id,))
        query_db('COMMIT;')
        return '', 204

    @app.post('/api/roles')
    @app.doc(description='Create a role', responses=[201,  409])
    @app.input(RoleIn, location='json', example=RoleIn.example())
    def create_role(json_data):
        role_id = query_db('INSERT INTO "roles" ("name") VALUES (?);', (json_data['name'],)) if not query_db('SELECT "name" FROM "roles" WHERE "name" = ? LIMIT 1;', (json_data['name'],), one=True) else abort(409, detail={"field": "name", "issue": f"Role already exists: {json_data['name']}"})
        query_db('COMMIT;')
        return {'message': 'Role created successfully!', 'id': role_id}, 201

    @app.get('/api/roles')
    @app.doc(description='Retrieve list roles', responses=[200, 404])
    @app.output(RolesOut(many=True), example=RolesOut.example())
    def read_roles():
        results = [dict(result) for result in query_db('SELECT * FROM "roles"')] or abort(404, detail='Roles not found')

        for result in results:
            result['url'] = url_for('read_role', id=result['id'], _external=True)
            del result['id']
        
        return results, 200

    @app.get('/api/roles/<int:id>')
    @app.doc(description='Single role', responses=[200,  404])
    def read_role(id):
        result = dict(query_db('SELECT * FROM "roles" WHERE "id" = ?', (id,), one=True)) or abort(404, detail='Role not found')
        return result, 200
    
    @app.patch('/api/roles/<int:id>')
    @app.doc(description='Update a role', responses=[204,  404])
    @app.input(RoleIn, location='json', example=RoleIn.example())
    @app.output(EmptySchema, status_code=204)
    def update_role(id, json_data):
        query_db('UPDATE "roles" SET "name" = ? WHERE "id" = ?;', (json_data['name'], id,)) or abort(404, detail='Role not found')
        query_db('COMMIT;')
        return '', 204

    @app.delete('/api/roles/<int:id>')
    @app.doc(description='Delete a role', responses=[204])
    @app.output(EmptySchema, status_code=204)
    def delete_role(id):
        query_db('DELETE FROM "roles" WHERE "id" = ?;', (id,))
        query_db('COMMIT;')
        return '', 204


def init_upload_routes(app):
    @app.get('/upload/<path:filename>')
    def read_upload(filename):
        return send_from_directory(app.config['UPLOAD_DIR'], filename)
    