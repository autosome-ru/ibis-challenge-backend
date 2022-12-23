from flask_restx import fields
from competition_app import api

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
