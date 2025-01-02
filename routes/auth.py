from apiflask import APIBlueprint, HTTPTokenAuth, abort
from authlib.jose import jwt, JoseError
from datetime import datetime, timezone, timedelta
from db import query_db
from flask import current_app, url_for
from schemas import UserIn, UserOut, CreatedSchema, Token, AuthorizationHeader
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPTokenAuth(scheme='Bearer')


def generate_token(user_id):
    header = {'alg': current_app.config['JWT_ALGORITHM']}
    payload = {'id': user_id, 'exp': (datetime.now(timezone.utc) + timedelta(minutes=60)).timestamp()}
    
    token = jwt.encode(header, payload, current_app.config['SECRET_KEY'])
    return token.decode('utf-8')


@auth.verify_token
def verify_token(token):
    try:
        payload = jwt.decode(token.encode("utf-8"), current_app.config['SECRET_KEY'])

        if datetime.now(timezone.utc).timestamp() > payload['exp']:
            abort(401, message='Access token has expired.', detail='Access token has expired.')

        id = payload['id']
        
        user = query_db('SELECT * FROM "users" WHERE "id" = ? LIMIT 1;', (id,), one=True)
    except JoseError:
        abort(401, detail='Invalid access token')
    return user


@auth.get_user_roles
def get_user_roles(user):
    role = 'admin' if user['is_admin'] else 'user'
    return role


authentication = APIBlueprint('authentication', __name__)


@authentication.post('/register')
@authentication.doc(description='Register a user', responses=[201, 409])
@authentication.input(UserIn, location='json', example=UserIn.example())
@authentication.output(CreatedSchema, 201, example=CreatedSchema.example())
def register(json_data):
    username = json_data.get('username')
    password = json_data.get('password')

    if ' ' in username: 
        abort(422, message='Invalid username: Username must not contain whitespaces.', detail='Username should not contain spaces.')

    user_id = query_db('INSERT INTO "users" ("username", "password") VALUES (?, ?);',
                (username, generate_password_hash(password),)) if not query_db('SELECT "username" FROM "users" WHERE "username" = ? LIMIT 1;', 
                                                                                (username,), one=True) else abort(409, message='Username already exists.', detail='Username already exists.')
    query_db('COMMIT;')

    return {'message': 'Registration successful.', 'id': user_id}, 201


@authentication.post('/login')
@authentication.doc(description='Authenticate a user', responses=[200, 401])
@authentication.input(UserIn, location='json', example=UserIn.example())
@authentication.output(Token, 200, example=Token.example(), description='Include the token inside Authorization Headers to access protected resources')
def login(json_data):
    username = json_data.get('username')
    password = json_data.get('password')

    user = query_db('SELECT "id", "password", "is_admin" FROM "users" WHERE "username" = ? LIMIT 1;', (username,), one=True)

    if not user or not check_password_hash(user['password'], password):
        abort(401, message='Credentials do not match.', detail="Invalid username or password")

    token = generate_token(user['id'])

    return {'token': f'Bearer {token}', 'is_admin': user['is_admin']}, 200

@authentication.get('/me')
@authentication.auth_required(auth)
@authentication.doc(description='Get current user', responses=[200])
@authentication.input(AuthorizationHeader, location='headers')
@authentication.output(UserOut, 200, example=UserOut.example())
def get_me(headers_data):
    user_info = dict(query_db('''SELECT "users"."id", 
                            "users"."username",
                            "users"."created_at", 
                            "user_profiles"."name", 
                            "user_profiles"."avatar"
                            FROM "users"
                            INNER JOIN "user_profiles" 
                            ON "user_profiles"."user_id" = "users"."id"
                            WHERE "id" = ?;''', 
                            (auth.current_user['id'],), one=True))
    
    user_info['created_at'] = datetime.fromtimestamp(user_info['created_at'], timezone.utc)
    user_info['avatar'] = url_for('read_upload', filename=user_info['avatar'], _external=True) if user_info['avatar'] else None

    return user_info, 200