from functools import wraps
from flask import g, request
from competition_app import api, logger
from competition_app.constants import roles
from competition_app.service import services


def get_token():
    parsed_words = request.headers.get('Authorization', '').split()
    logger.info('|%s| parsed header: %s', "get_token", ", ".join(parsed_words))
    if len(parsed_words) != 2 or parsed_words[0] != 'Bearer':
        return None
    return parsed_words[1]


def role_required(role_id=len(roles) - 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.info('|%s| is called', "role_required")
                g.current_user = user = services.get_user(get_token(), 'token')
                if user is None:
                    logger.info('|%s| user is NONE', "role_required")
                    raise ValueError
                current_role = user.role
                logger.info('|%s| role of user: %s', "role_required", current_role)
                if not services.check_last_seen(user):
                    logger.info('|%s| token of user expired', "role_required")
                    api.abort(403, 'token expired')
            except ValueError:
                logger.info('|%s| some error, invalid token', "role_required")
                api.abort(401, 'invalid token')

            services.update_last_seen(user)
            current_role_index = roles.index(current_role)
            if current_role_index > role_id:
                api.abort(403, 'Access denied')

            return func(*args, **kwargs)

        return wrapper

    return decorator
