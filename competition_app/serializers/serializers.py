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

# team

team_model_base = api.model('Basic team model', {
    'name': fields.String,
    'contact_email': fields.String
})

member_model_base = api.model('Basic member model', {
    'name': fields.String,
    'affiliation': fields.String,
    'country': fields.String,
    'city': fields.String,
    'member_idx': fields.Integer
})

team_model_with_members = api.clone('Team model with members', team_model_base, {
    'members': fields.List(fields.Nested(member_model_base))
})

