# Exceptions
class EagleeyenetworksError(Exception):

    def __init__(self, message=None, http_body=None, http_status=None,
                 json_body=None):
        super(EagleeyenetworksError, self).__init__(message)

        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf-8')
            except:
                http_body = ('<Could not decode body as utf-8. '
                             'Please report to support@eagleeyenetworks.com>')

        self.http_body = http_body

        self.http_status = http_status
        self.json_body = json_body


class APIError(EagleeyenetworksError):
    pass


class APIConnectionError(EagleeyenetworksError):
    pass


class InvalidRequestError(EagleeyenetworksError):

    def __init__(self, message, param, http_body=None,
                 http_status=None, json_body=None):
        super(InvalidRequestError, self).__init__(
            message, http_body, http_status, json_body)
        self.param = param


class AuthenticationError(EagleeyenetworksError):
    pass
