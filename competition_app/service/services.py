from datetime import datetime
from uuid import uuid4
from competition_app.models import User, Team, TeamsMembers
from competition_app import session, db, logger


def get_user(value, by='user_id'):
    if by == 'user_id':
        return User.query.get_or_404(value)
    elif by == 'token':
        logger.info('|%s| token received %s', "get_user", value)
        return User.query.filter_by(token=value).one_or_none()
    else:
        raise ValueError


def get_user_or_none(value, by='user_id'):
    if by == 'user_id':
        return User.query.filter_by(user_id=value).one_or_none()
    elif by == 'token':
        logger.info('|%s| token received %s', "get_user_or_none", value)
        return User.query.filter_by(token=value).one_or_none()
    else:
        raise ValueError


def create_database_item(cls, data, include=None, exclude=tuple()):
    return cls(
        **{k: v for k, v in data.items() if k not in exclude and (k in include if include is not None else True)})


def check_last_seen(user):
    if user.token is None:
        return False
    time_since_last_seen = datetime.now() - user.last_seen
    # TODO WARNING! might reconsider expiration time of of tokens
    is_expired = time_since_last_seen.days > 0 or time_since_last_seen.seconds >= 48 * 3600
    # TODO TEST VALUE
    #is_expired = time_since_last_seen.seconds >= 0
    logger.info('|%s| time elapsed %d of %d seconds, (%s)', "check_last_seen", time_since_last_seen.seconds, 48 * 3600,
                is_expired)
    logger.info('|%s| result is %s, %s', "check_last_seen", not is_expired, "expired" if is_expired else "not expired")

    return not is_expired


def generate_token():
    return str(uuid4())


def update_user_token(user):
    logger.info('|%s| updating user token', "update_user_token")
    user.token = generate_token()
    session.commit()


def update_last_seen(user):
    logger.info('|%s| updating user last seen', "update_last_seen")
    # if not check_last_seen(user):
    #     # update_user_token(user)
    #     user.token = generate_token()
    user.last_seen = db.func.now()
    session.commit()


def patch_user(user, data):
    for attr, value in data.items():
        if attr != 'user_id':
            setattr(user, attr, value)
    session.commit()
    update_last_seen(user)
    return user


# def patch_user_by_id(user_id, data):
#     user = get_user(user_id)
#     for attr, value in data.items():
#         if attr != 'user_id':
#             setattr(user, attr, value)
#     session.commit()
#     update_last_seen(user)  # IDK if it's actually good
#     return user


def register_user(data):
    user = get_user_or_none(data['user_id'])
    user_not_exists = user is None
    if user_not_exists:
        user = create_database_item(User, data)
        session.add(user)
    if not check_last_seen(user):
        update_last_seen(user)
        update_user_token(user)
    patch_user(user, data)
    session.commit()
    return user_not_exists, user


def delete_user(user_id):
    user = get_user(user_id)
    session.delete(user)
    session.commit()


def update_or_create_team(user, data):
    print("update_or_create_team", user.team)
    team_data = dict()
    team_data['contact_email'] = data['email']
    team_data['name'] = data['name']
    team_data['user_id'] = user.user_id

    if user.team is None:
        user.team = Team(**team_data)
        session.add(user.team)
    else:
        for attr, value in team_data.items():
            if attr != 'user_id':
                setattr(user.team, attr, value)
    session.commit()

    members_data = data['members']
    for member in members_data:
        member['team_id'] = user.team.team_id

    user.team.members = [TeamsMembers(**member) for member in members_data]
    for member in user.team.members:
        session.add(member)
    session.commit()

    return user.team
