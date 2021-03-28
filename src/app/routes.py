from src.app.api import *

auth_blueprint = Blueprint('auth', __name__)

auth_blueprint.add_url_rule(
    '/',
    view_func=index_view,
    methods=['GET']
)

auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
