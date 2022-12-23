from flask_restx import fields
from competition_app import api

# submit

challenge_discipline_model = api.model('All information about discipline', {
    'name': fields.String(default='1'),
    'view': fields.String(default='1'),
    'comment': fields.String(default='1'),
})

challenge_tf_model = api.model('All information about tf', {
    'name': fields.String(default='1'),
    'view': fields.String(default='1'),
    'comment': fields.String(default='1'),
})

challenge_method_model = api.model('All information about method', {
    'name': fields.String(default='1'),
    'view': fields.String(default='1'),
    'comment': fields.String(default='1'),
})

challenge_metrics_info = api.model('Info about metrics for specific discipline', {
    'discipline': fields.String(),
    'metrics': fields.List(fields.String())
})

challenge_general_info_model = api.model('All information about leaderboard and final', {
    # 'methods': fields.List(fields.Nested(challenge_method_model)),
    'disciplines': fields.List(fields.Nested(challenge_discipline_model)),
    'tfs': fields.List(fields.Nested(challenge_tf_model)),
    'metrics': fields.List(fields.Nested(challenge_metrics_info))
})
