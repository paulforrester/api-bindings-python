from .base import ImageResource, InstanceResource


class Asset(ImageResource):
    pass


_asset = Asset('/asset/asset/image.jpg', 'get')

def asset(session, esn, tm, type='pre', quality='high'):
    return _asset(session, c=esn, t=tm, a=type, q=quality)