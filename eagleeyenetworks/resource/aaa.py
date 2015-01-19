from .base import ActionResource, InstanceResource, JsonMixin


class AuthenticateToken(InstanceResource):
    pass


class AuthorizeUser(InstanceResource):
    pass


class Authenticate(JsonMixin, ActionResource):
    pass


class Authorize(JsonMixin, ActionResource):
    def post_call(self, session, new_obj=None):
        super(Authorize, self).post_create(session, new_obj)
        session._au = new_obj


class Logout(ActionResource):
    def post_call(self, session, new_obj=None):
        super(Logout, self).post_create(session, new_obj)
        session._au = new_obj

authenticate = Authenticate('/g/aaa/authenticate', 'post', cls=AuthenticateToken)
authorize = Authorize('/g/aaa/authorize', 'post', cls=AuthorizeUser)
logout = Logout('/g/aaa/logout', 'post')

# Convenience method not included in API
def login(session, username, password):
    authenticate_result = authenticate(session, username=username, password=password)
    return authorize(session, token=authenticate_result.token)