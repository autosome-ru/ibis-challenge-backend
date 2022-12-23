from flask import g, request
from flask_restx import Resource

from competition_app import api
from competition_app.routes.auth_routes import auth_nsp
from competition_app.routes.global_routes import role_required
from competition_app.serializers import team_model_with_members, token_model_base
from competition_app.service import update_or_create_team


@auth_nsp.route('/team')
class Team(Resource):
    @api.marshal_with(team_model_with_members)
    @role_required(1)
    def get(self):
        print(g.current_user.team)
        return g.current_user.team

    @api.marshal_with(team_model_with_members)
    @api.expect(team_model_with_members)
    @role_required(1)
    def post(self):
        update_or_create_team(g.current_user, request.get_json())
        print(g.current_user.team.members)
        return g.current_user.team
