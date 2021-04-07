from flask import Blueprint
from .api import *

api_blueprint = Blueprint('api', __name__)


api_blueprint.add_url_rule(
    '/',
    view_func=index_view,
    methods=['GET']
)

api_blueprint.add_url_rule(
    '/pegawai/auth/register',
    view_func=registration_view,
    methods=['POST']
)

api_blueprint.add_url_rule(
    '/pegawai/auth/login',
    view_func=login_view,
    methods=['POST']
)

api_blueprint.add_url_rule(
    '/pegawai/auth/status',
    view_func=pegawai_api,
    methods=['GET']
)
