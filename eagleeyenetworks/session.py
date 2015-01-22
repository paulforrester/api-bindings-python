import requests
from . import APIError, DEFAULT_BASE_URL

# Patch requests to add stream recv method


class Session(object):
    def __init__(self, apikey, apisecret='', baseurl=DEFAULT_BASE_URL):
        # Use a requests session object to maintain a login session with the cloud.
        self.session = requests.session()
        self.apikey = apikey
        self.apisecret = apisecret
        self.baseurl = baseurl
        self.authentication_user = None

    def request(self, method, uri,  body=None, urlparams=None, headers=None):
        # convert the kwargs to a json string so we can sign the request if needed
        resp = self.session.request(method,
                               self.baseurl+uri,
                               data=body,
                               params=urlparams,
                               headers=headers,
                               auth=(self.apikey, self.apisecret))
        if 200 <= resp.status_code < 300:
            try:
                if 'application/json' in resp.headers.get('content-type', ''):
                    return resp.json(), resp.headers
                else:
                    return resp.content, resp.headers
            except:
                raise APIError(
                    "Invalid response body from API: %s "
                    "(HTTP response code was %d)" % (resp.content, resp.status_code),
                    http_body=resp.content, http_status=resp.status_code, url=resp.url)
        elif resp.status_code == 401 or resp.status_code == 403:
            raise APIError(
                "Authentication Error from API: %s "
                "(HTTP response code was %d)" % (resp.content, resp.status_code),
                http_body=resp.content, http_status=resp.status_code, url=resp.url)
        else:
            raise APIError(
                "Error from API: %s "
                "(HTTP response code was %d)" % (resp.content, resp.status_code),
                http_body=resp.content, http_status=resp.status_code, url=resp.url)
