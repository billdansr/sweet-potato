from apiflask import Schema
from apiflask.fields import String, Integer, Date, URL, List, Dict, File, DateTime, Float
from apiflask.schemas import EmptySchema
from apiflask.validators import FileSize, FileType, Range


class Token(Schema):
    token = String(required=True)
    is_admin = Integer(required=True, validate=Range(min=0, max=1))

    @staticmethod
    def example():
        return {
            "token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiYWRtaW4iOjAsImV4cCI6MTczNDM1MTMzMi45MjYzOTh9.Dh--bIms6bq6UseB11eGUvCeNwfb-ub0vD4Jq5LXlN8",
            "is_admin": 1
        }


class AuthorizationHeader(Schema):
    authorization = String(required=True, metadata={
        'description': 'Authorization header in the format: Bearer <access_token>'
    })


class UserProfileIn(Schema):
    name = String(required=True, allow_none=False)
    avatar = File(allow_none=True, validate=[FileType(['.png', '.jpg', '.jpeg']), FileSize(max='5 MB')])


class UserIn(Schema):
    username = String(required=True)
    password = String(required=True)

    @staticmethod
    def example():
        return {
            'username': 'ohayou',
            'password': 'ohayou123'
        }


class UserOut(Schema):
    id = Integer(required=True)
    username = String(required=True)
    name = String()
    avatar = URL()
    created_at = DateTime()

    @staticmethod
    def example():
        return {
            'id': 1,
            'username': 'ohayou',
            'name': 'ohayou',
            'avatar': 'https://example.com/avatar.png'
        }


class GameIn(Schema):
    title = String(required=True)
    description = String()
    release_date = Date(allow_none=True)
    genres = List(String)
    platforms = List(String)
    companies = List(String)
    media = List(File(validate=[FileType(['.png', '.jpg', '.jpeg', '.gif', '.mp4']), FileSize(max='100 MB')]), allow_none=True)
    thumbnail = File(validate=[FileType(['.png', '.jpg', '.jpeg']), FileSize(max='100 MB')], allow_none=True)


class GameOut(Schema):
    id = Integer(required=True)
    title = String(required=True)
    description = String()
    release_date = Date(allow_none=True)
    thumbnail = String()
    media = String()
    genres = List(Dict)
    platforms = List(Dict)
    companies = List(Dict)
    average_rating = Float(validate=Range(min=0, max=5))

    @staticmethod
    def example():
        return {
            'id': 1,
            'title': 'The Legend of Zelda: Breath of the Wild',
            'description': 'The Legend of Zelda: Breath of the Wild is an action-adventure game developed and published by Nintendo for the Nintendo Switch and Wii U.',
            'release_date': '2017-03-03',
            'thumbnail': 'https://example.com/image.jpg',
            'media': 'https://example.com/1/media',
            'genres': [
                {
                    'name': 'Action',
                    'url': 'https://example.com/genres/1'
                },
                {
                    'name': 'Adventure',
                    'url': 'https://example.com/genres/2'
                }
            ],
            'platforms': [
                {
                    'name': 'Nintendo Switch',
                    'url': 'https://example.com/platforms/1'
                },
                {
                    'name': 'Wii U',
                    'url': 'https://example.com/platforms/2'
                }
            ],
            'companies': [
                {
                    'name': 'Nintendo',
                    'url': 'https://example.com/companies/1'
                }
            ],
            'average_rating': 4.5
        }


class GamesOut(Schema):
    count = Integer(required=True)
    next = String(allow_none=True)
    previous = String(allow_none=True)
    results = List(Dict)

    @staticmethod
    def example():
        return {
            'count': 6,
            'next': 'https://example.com/games/?offset=4&limit=2',
            'previous': 'https://example.com/games/?offset=0&limit=2',
            'results': [
                {
                    "title": "The Legend of Zelda: Breath of the Wild",
                    "url": "https://example.com/games/1"
                },
                {
                    "title": "The Legend of Zelda: Twilight Princess",
                    "url": "https://example.com/games/2"
                }
            ]
        }
    

class GamesQuery(Schema):
    offset = Integer(load_default=0)
    limit = Integer(load_default=20)
    search = String(load_default='')
    

class GenreIn(Schema):
    name = String(required=True)

    @staticmethod
    def example():
        return {
            'name': 'Action'
        }


class GenreOut(Schema):
    id = Integer(required=True)
    name = String(required=True)

    @staticmethod
    def example():
        return {
            'id': 1,
            'name': 'Action'
        }


class GenresOut(Schema):
    name = String(required=True)
    url = URL()

    @staticmethod
    def example():
        return [
            {
                'name': 'Action',
                'url': 'https://example.com/genres/1'
            }
        ]


class PlatformIn(Schema):
    name = String(required=True)

    @staticmethod
    def example():
        return {
            'name': 'Nintendo Switch'
        }


class PlatformOut(Schema):
    id = Integer(required=True)
    name = String(required=True)

    @staticmethod
    def example():
        return {
            'id': 1,
            'name': 'Nintendo Switch'
        }


class PlatformsOut(Schema):
    name = String(required=True)
    url = URL()

    @staticmethod
    def example():
        return [
            {
                'name': 'Nintendo Switch',
                'url': 'https://example.com/platforms/1'
            }
        ]


class CompanyIn(Schema):
    name = String(required=True)
    founding_date = Date(allow_none=True)
    headquarters = List(String)
    roles = List(String)

    @staticmethod
    def example():
        return {
            'name': 'Nintendo',
            'founding_date': '1889-09-23',
            'headquarters': ['Kyoto, Japan'],
            'roles': ['Developer', 'Publisher']
        }
    

class CompanyOut(Schema):
    id = Integer(required=True)
    name = String(required=True)
    founding_date = Date()
    headquarters = List(String)
    roles = List(Dict)

    @staticmethod
    def example():
        return {
            'id': 1,
            'name': 'Nintendo',
            'founding_date': '1889-09-23',
            'headquarters': ['Kyoto, Japan'],
            'roles': [
                {
                    'name': 'Developer',
                    'url': 'https://example.com/roles/1'
                },
                {
                    'name': 'Publisher',
                    'url': 'https://example.com/roles/2'
                }
            ]
        }
    

class CompaniesOut(Schema):
    name = String(required=True)
    url = URL()

    @staticmethod
    def example():
        return [
            {
                'name': 'Nintendo',
                'url': 'https://example.com/companies/1'
            }
        ]
    

class RoleIn(Schema):
    name = String(required=True)

    @staticmethod
    def example():
        return {
            'name': 'Engine Developer'
        }


class RoleOut(Schema):
    id = Integer(required=True)
    name = String(required=True)

    @staticmethod
    def example():
        return {
            'id': 1,
            'name': 'Engine Developer'
        }
    

class RolesOut(Schema):
    name = String(required=True)
    url = URL()

    @staticmethod
    def example():
        return [
            {
                'name': 'Engine Developer',
                'url': 'https://example.com/roles'
            }
        ]
    

class CreatedSchema(Schema):
    message = String(required=True)
    id = Integer(required=True)

    @staticmethod
    def example():
        return {
            'message': 'Data created successfully!',
            'id': 1
        }
    

class UpdatedSchema(Schema):
    message = String(required=True)

    @staticmethod
    def example():
        return {
            'message': 'Data updated successfully!'
        }
    

class RatingIn(Schema):
    game_id = Integer(required=True)
    score = Integer(required=True, validate=Range(min=0, max=5))
    review = String(allow_none=True)

    @staticmethod
    def example():
        return {
            'game_id': 1,
            'score': 5,
            'review': 'This game is amazing!'
        }
    
class RatingOut(Schema):
    avatar = URL(allow_none=True)
    user = String(required=True)
    game = String(required=True)
    score = Integer(required=True, validate=Range(min=0, max=5))
    review = String(allow_none=True)
    created_at = DateTime()
    updated_at = DateTime(allow_none=True)

    @staticmethod
    def example():
        return {
            'avatar': 'https://example.com/avatar.png',
            'user': 'ohayou',
            'game': 'The Legend of Zelda: Breath of the Wild',
            'score': 5,
            'review': 'This game is amazing!',
            'created_at': '2021-01-01T00:00:00Z',
            'updated_at': '2021-01-01T00:00:00Z'
        }
