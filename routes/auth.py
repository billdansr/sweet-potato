from apiflask import APIBlueprint, HTTPTokenAuth, abort
from authlib.jose import jwt, JoseError
from datetime import datetime, timezone, timedelta
from db import query_db
from flask import current_app
from schemas import UserIn, UserOut, CreatedSchema, Token
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPTokenAuth(scheme='Bearer')


def generate_token(user_id):
    is_admin = query_db('SELECT "is_admin" FROM "users" WHERE "id" = ? LIMIT 1;', (user_id,), one=True)['is_admin']

    header = {'alg': current_app.config['JWT_ALGORITHM']}
    payload = {'id': user_id, 'admin': is_admin, 'exp': (datetime.now(timezone.utc) + timedelta(minutes=20)).timestamp()}
    
    token = jwt.encode(header, payload, current_app.config['SECRET_KEY'])
    return token.decode('utf-8')


@auth.verify_token
def verify_token(token):
    try:
        payload = jwt.decode(token.encode("utf-8"), current_app.config['SECRET_KEY'])

        if datetime.now(timezone.utc).timestamp() > payload['exp']:
            abort(401, detail='Access token has expired')

        id = payload['id']
        
        user = query_db('SELECT * FROM "users" WHERE "id" = ? LIMIT 1;', (id,), one=True)
    except JoseError:
        abort(401, detail='Invalid access token')
    return user


authentication = APIBlueprint('authentication', __name__, url_prefix='/auth')


@authentication.post('/register')
@authentication.doc(description='Register a user', responses=[201, 409])
@authentication.input(UserIn, location='json', example=UserIn.example())
@authentication.output(CreatedSchema, 201, example=CreatedSchema.example())
def register(json_data):
    username = json_data.get('username')
    password = json_data.get('password')

    user_id = query_db('INSERT INTO "users" ("username", "password") VALUES (?, ?);',
                (username, generate_password_hash(password),)) if not query_db('SELECT "username" FROM "users" WHERE "username" = ? LIMIT 1;', 
                                                                                (username,), one=True) else abort(409, detail='Username already exists.')

    query_db('COMMIT;')

    return {'message': 'Registration successful.', 'id': user_id}, 201


@authentication.post('/login')
@authentication.doc(description='Authenticate a user', responses=[200, 401])
@authentication.input(UserIn, location='json', example=UserIn.example())
@authentication.output(Token, 200, example=Token.example(), description='Include the token inside Authorization Headers to access protected resources')
def login(json_data):
    username = json_data.get('username')
    password = json_data.get('password')

    user = query_db('SELECT "id", "password" FROM "users" WHERE "username" = ? LIMIT 1;', (username,), one=True)

    if not user or not check_password_hash(user['password'], password):
        abort(401, detail="Invalid username or password")

    token = generate_token(user['id'])

    return {'token': f'Bearer {token}'}, 200
