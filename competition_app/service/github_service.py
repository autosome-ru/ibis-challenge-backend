from urllib import parse

from competition_app import api, github_config, logger
import requests


def check_github_code(code):
    if code == "":
        return False
    return True


def check_github_access_token(token):
    if token == "":
        return False
    return True


def fetch_github_access_token(code):
    payload = {'client_id': github_config["client_id"],
               'client_secret': github_config["client_secret"],
               'code': code,
               'redirect_uri': github_config["redirect_uri"]}
    # params = parse.urlencode(payload)
    # full_url = f'{github_config["github_access_token_api_url"]}?{params}'

    github_request = requests.post(github_config["github_access_token_api_url"], params=payload)
    logger.info('|%s| fetched url: %s', "fetch_github_access_token", github_request.url)

    if github_request.status_code != 200:
        logger.info('|%s| unable to fetch GitHub access token', "fetch_github_access_token")
        result = dict()
    else:
        result = dict(parse.parse_qsl(github_request.text))
        if "access_token" not in result:
            logger.info('|%s| GitHub provided no access token', "fetch_github_access_token")
            result = dict()
        else:
            logger.info('|%s| GitHub provided access token: %s', "fetch_github_access_token", result['access_token'])

    return bool(result), result


def fetch_github_user(access_token):
    github_request = requests.get(github_config["github_user_api_url"],
                                  headers={"Authorization": f"Bearer {access_token}"})

    if github_request.status_code != 200:
        logger.info('|%s| unable to fetch GitHub user', "fetch_github_user")
        result = dict()
    else:
        full_result = github_request.json()
        result = {k: full_result[k] for k in ['id', 'avatar_url', 'login', 'name']}
        result['user_id'] = result.pop('id')
        result['access_token'] = access_token
        print(result)

    return bool(result), result
