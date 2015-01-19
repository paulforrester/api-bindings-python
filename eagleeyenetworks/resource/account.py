from .base import InstanceResource, JsonMixin, UpdateableAPIResourceMixin


class Account(UpdateableAPIResourceMixin, JsonMixin, InstanceResource):
    uri = '/g/account'
    list_uri = '/g/account/list'
