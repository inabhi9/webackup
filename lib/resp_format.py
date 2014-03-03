from flask import request, abort
import json

JSON_CONTENT_TYPE = 'text/x-json'

def from_dict(status, data=None, err=None, fmt='json', httpcode=200, msg=None, **kwargs):
    
    '''Generating response object'''
    resp = {}
    resp['payload'] = {'status': status, 'msg':msg}
    if data: resp['payload'].update({'data': data})
    if err: resp['payload'].update({'error':err})
    resp.update(**kwargs)
    
    '''Managin HTTP status code'''
    # if request.args.get('suppress_http_code', '').lower() == 'true':
    resp['http_status_code'] = httpcode
    resp['http_code_msg'] = HTTP_CODE_MSG[httpcode]
    httpcode = 200
    
    if httpcode == 400: abort(httpcode)
    
    '''Returning Response object'''
    if fmt == 'json': return (json.dumps(resp), httpcode, {'Content-Type':JSON_CONTENT_TYPE})
    
MSG_FAIL = "error"
MSG_OK = "success"

'''Http error codes'''
HTTP_200 = 200  # OK
HTTP_201 = 201  # Created
HTTP_202 = 202  # Accepted
HTTP_204 = 204  # No Content
HTTP_410 = 410  # Gone - For removing, Deleted
HTTP_401 = 401  # Unauthorized
HTTP_400 = 400  # Bad Request
HTTP_412 = 412  # The server does not meet one of the preconditions that the requester put on the request
HTTP_422 = 422  # Unprocessable Entity
HTTP_404 = 404  # Not Found

HTTP_CODE_MSG = {
    400: "Not found",
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No content",
    410: "Gone",
    401: "Unauthorized request",
    400: "Bad Request",
    412: "The server does not meet one of the preconditions that the requester put on the request",
    422: "Unprocessable Entity"
}
