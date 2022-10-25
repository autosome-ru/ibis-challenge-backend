from flask_restx import Resource
from competition_app import api, logger
from flask import request, g
from competition_app.routes.global_routes import role_required
from competition_app.serializers.serializers import github_code_model, token_model_base, user_account_model_data
from competition_app.service import services, github_service

auth_nsp = api.namespace('Authorization', path='/auth', description='Operations related to authentication')


@auth_nsp.route('')
class CodeAuth(Resource):
    """
    Authorization via GitHub code
    """

    @api.marshal_with(token_model_base)
    @api.expect(github_code_model)
    @api.response(403, 'Invalid authorization code')
    def post(self):
        code = request.get_json()['code']

        if not github_service.check_github_code(code):
            api.abort(406, 'Authorization code is wrong')

        # Step 1. Exchange authentication code given by GitHub (given to user client and sent by client to backend) for
        # access token of GitHub (for user api)
        acc_token_success, acc_token_result = github_service.fetch_github_access_token(code)
        if not acc_token_success:
            api.abort(406, 'Fetching of GitHub access token was unsuccessful')

        # Step 2. Extract access token from GitHub response
        access_token = acc_token_result["access_token"]

        # Step 3. Request user data from GitHub given the access token
        user_success, user_result = github_service.fetch_github_user(access_token)
        if not user_success:
            api.abort(406, 'Fetching of GitHub user was unsuccessful')

        exists, user = services.register_user(user_result)
        logger.info('|%s| user exists? - %s', "CodeAuth/post", exists)
        return user


@auth_nsp.route('/profile')
class UserProfile(Resource):
    """
    User profile for given token
    """

    @api.marshal_with(user_account_model_data)
    @api.expect(token_model_base)
    @api.response(403, 'Access denied')
    @role_required(1)
    def get(self):
        print(g.current_user)
        return g.current_user
