import os
from apiflask import APIBlueprint, abort
from datetime import datetime, timezone
from db import query_db
from flask import current_app, url_for
from routes import auth
from schemas import UserProfileIn, UserOut, EmptySchema, AuthorizationHeader
from werkzeug.utils import secure_filename

user = APIBlueprint('user', __name__)


@user.get('/<int:id>')
@user.doc(description='User profile', responses=[200, 404])
@user.output(UserOut, 200, example=UserOut.example())
def read_user(id):
    result = dict(query_db('''SELECT "users"."id", 
                            "users"."username",
                            "users"."created_at", 
                            "user_profiles"."name", 
                            "user_profiles"."avatar"
                            FROM "users"
                            INNER JOIN "user_profiles" 
                            ON "user_profiles"."user_id" = "users"."id"
                            WHERE "id" = ?;''', 
                            (id,), one=True) or abort(404, detail='User not found'))
    
    result['created_at'] = datetime.fromtimestamp(result['created_at'], timezone.utc)
    result['avatar'] = url_for('read_upload', filename=result['avatar'], _external=True)

    return result, 200


@user.patch('/')
@user.auth_required(auth)
@user.doc(description='Update user profile', responses=[204])
@user.input(AuthorizationHeader, location='headers')
@user.input(UserProfileIn, location='files')
@user.output(EmptySchema, 204)
def update_user(files_data):
    user = auth.current_user
    name = files_data.get('name')
    avatar = files_data.get('avatar')

    query_db('UPDATE "user_profiles" SET "name" = ? WHERE "user_id" = ?;', (name, user['id'],))

    if avatar:        
        filename = secure_filename(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S%z') + '_' + avatar.filename)
        avatar.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
        query_db('UPDATE "user_profiles" SET "avatar" = ? WHERE "user_id" = ?;', (filename, id,))

    query_db('COMMIT;')

    return '', 204
