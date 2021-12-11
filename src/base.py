import json

from bottle import Bottle, response


class JsonBottle(Bottle):
    def default_error_handler(self, res):
        response.content_type = "application/json"
        return json.dumps(dict(error=res.body, status_code=res.status_code))
