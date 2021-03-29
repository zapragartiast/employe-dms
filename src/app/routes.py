from src.app.api import *

auth_blueprint = Blueprint('auth', __name__)

auth_blueprint.add_url_rule(
    '/',
    view_func=index_view,
    methods=['GET']
)

auth_blueprint.add_url_rule(
    '/pegawai/auth/register',
    view_func=registration_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/pegawai/auth/login',
    view_func=login_view,
    methods=['POST']
)
