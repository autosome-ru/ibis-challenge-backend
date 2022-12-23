from flask_restx import fields
from competition_app import api

# user

github_code_model = api.model('Github auth code model', {
    'code': fields.String
})

user_model_base = api.model('Basic user model', {
    'user_id': fields.Integer(min=1, readonly=True),
    'avatar_url': fields.String,
    'login': fields.String,
    'name': fields.String,
    'joined_since': fields.String
})

user_model_with_token = api.clone('User model with token', user_model_base, {
    'token': fields.String,
})

user_account_model_data = api.model('Basic user model', {
    'avatar_url': fields.String,
    'login': fields.String,
    'name': fields.String,
    'joined_since': fields.String
})

token_model_base = api.model('Basic token model', {
    'token': fields.String,
})
