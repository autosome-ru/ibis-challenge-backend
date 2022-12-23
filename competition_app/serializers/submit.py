from flask_restx import fields
from competition_app import api

# submit

# submit_model = api.model('Single submit model', {
#     'submit_id': fields.Integer,
#     'submit_info': fields.String,
#     'submit_metrics': fields.List(fields.Float),
#     'submit_ranks': fields.List(fields.Integer),
#     'submit_aggregated_rank': fields.Integer
# })
#
# submits_model = api.model('List of submits model', {
#     'metrics_order': fields.List(fields.String),
#     'submits': fields.List(fields.Nested(submit_model)),
#     'discipline_name': fields.String,
#     'tf_name': fields.String,
# })

submit_model = api.model('Single submit model', {
    'id': fields.Integer,
    'name': fields.String,
    'info': fields.String,
    'metrics': fields.List(fields.Float),
    'ranks': fields.List(fields.Integer),
    'team': fields.String,
    'aggregated_rank': fields.Integer
})

submits_model = api.model('List of submits model', {
    'metrics_order': fields.List(fields.String),
    'submits': fields.List(fields.Nested(submit_model))
})
