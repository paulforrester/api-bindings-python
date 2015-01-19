from .base import InstanceResource, JsonMixin, UpdateableAPIResourceMixin


class Device(UpdateableAPIResourceMixin, JsonMixin, InstanceResource):
    uri = '/g/device'
    list_uri = '/g/device/list'
