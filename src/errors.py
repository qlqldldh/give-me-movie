from bottle import HTTPError

from src.enums import HttpStatus


class HTTPNotFoundError(HTTPError):
    def __init__(self, body=None, exception=None, traceback=None, **options):
        status = HttpStatus.NOT_FOUND
        super(HTTPNotFoundError, self).__init__(
            status.value, body, exception, traceback ** options
        )


class HTTPBadRequestError(HTTPError):
    def __init__(self, body=None, exception=None, traceback=None, **options):
        status = HttpStatus.BAD_REQUEST
        super(HTTPBadRequestError, self).__init__(
            status.value, body, exception, traceback ** options
        )
