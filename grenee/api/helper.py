import json
from datetime import datetime, date
from werkzeug.wrappers import Response


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def response(data, status_code=200):
    response = Response(
        json.dumps(data, cls=CustomJSONEncoder), content_type="application/json"
    )
    response.status_code = status_code
    return response 
    