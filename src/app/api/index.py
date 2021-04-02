from flask import make_response, jsonify
from flask.views import MethodView


class IndexAPI(MethodView):
    def get(self):
        response_object = {
            'code': 200,
            'message': 'This API is works!'
        }
        return make_response(jsonify(response_object))


index_view = IndexAPI.as_view('index_api')
