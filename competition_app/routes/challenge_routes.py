import json
from flask_restx import Resource, fields

from competition_app import api, get_call_params
from competition_app.constants import stages, methods, disciplines_tfs_matrices, disciplines, tfs, all_disciplines, \
    all_tfs, challenge_general_info, get_disciplines_tf_array
from competition_app.serializers import challenge_general_info_model, submits_model
from competition_app.service.leaderboard_service import generate_team_submits

challenge_nsp = api.namespace('Challenge', path='/challenge',
                              description='Operations related to fetching leaderboard data')

params_parser = api.parser()
params_parser.add_argument('mode', choices=stages, location='args')
params_parser.add_argument('method', choices=methods, location='args')
params_parser.add_argument('tf', choices=all_tfs, location='args')
params_parser.add_argument('discipline', choices=all_disciplines, location='args')


@challenge_nsp.route('/info/general')
class ChallengeGeneralInfo(Resource):
    """
    General information about leaderboard
    """
    def get(self):
        #print(json.dumps(challenge_general_info))
        return json.dumps(challenge_general_info)

@challenge_nsp.route('/info/specific')
class ChallengeSpecificInfo(Resource):
    """
    Specific information about leaderboard
    """
    def get(self):
        #print(json.dumps(get_disciplines_tf_array()))
        return json.dumps(get_disciplines_tf_array())

@challenge_nsp.route('/submits')
class Submits(Resource):
    """
    Information about specified team's commits
    """

    @api.marshal_with(submits_model)
    def get(self):
        try:
            print("SUBMITS")
            print(stages, methods, all_disciplines, all_tfs)
            mode, method, discipline, tf = get_call_params(params_parser)
            #discipline = params_parser.parse_args()['discipline']
            print("SUBMITS", discipline, tf)
            #tf = "RORB"
            print(generate_team_submits(discipline, tf))
            return generate_team_submits(discipline, tf)
        except ValueError:
            api.abort(404)


@challenge_nsp.route('/team-submits')
class TeamSubmits(Resource):
    """
    Information about specified team's commits
    """

    @api.marshal_with(submits_model)
    def get(self):
        try:
            mode, tf, discipline = get_call_params(params_parser)
            return generate_team_submits(discipline, tf)
        except ValueError:
            api.abort(404)


@challenge_nsp.route('/tf-discipline')
class OneTfOneDiscipline(Resource):
    """

    """
