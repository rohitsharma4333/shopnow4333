from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(statusCode, message=None):
    payload = {
        'error': HTTP_STATUS_CODES.get(statusCode, 'Unknown error')
    }
    if(message):
        payload['message'] = message

    response = jsonify(payload)
    response.status_code = statusCode
    return(response)

#--------------------------------------------------------------------------------------

def bad_request(message):
    return(error_response(400, message))