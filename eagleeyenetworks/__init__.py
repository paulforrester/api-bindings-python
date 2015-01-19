# Eagleeyenetworks Python bindings
# API docs at http://apidocs.eagleeyenetworks.com/

from eagleeyenetworks.version import VERSION

DEFAULT_BASE_URL = 'https://login.eagleeyenetworks.com'


# Resource
from eagleeyenetworks.resource import *

from eagleeyenetworks.error import (
    EagleeyenetworksError, APIError, APIConnectionError, AuthenticationError,
    InvalidRequestError)

from eagleeyenetworks.session import Session

