from .. import VERSION
import simplejson as json
import sys
import logging

logger = logging.getLogger(__file__)


class Resource(dict):
    def prepare_to_send(self, method, body=None, **kwargs):
        urlparams = None
        if method.lower() in ('get', 'delete'):
            urlparams = kwargs
        headers = {
            'User-Agent': 'Eagleeyenetworks/v1 PythonBindings/%s' % (VERSION,)
        }
        return urlparams, body, headers

    def process_result(self, body, headers):
        return body, headers

    def post_create(self, session, *args):
        pass


class JsonMixin(object):
    def prepare_to_send(self, method, body=None, **kwargs):
        urlparams, body, headers = super(JsonMixin, self).prepare_to_send(method, body, **kwargs)
        if method.lower() in ('post', 'put'):
            if body:
                body = json.dumps(body)
            else:
                body = json.dumps(kwargs)
                urlparams = None
            headers['content-type'] = 'application/json'
        return urlparams, body, headers

    def process_result(self, body, headers):
        body, headers = super(JsonMixin, self).process_result(body, headers)
        if 'application/json' in headers.get('content-type', '') and isinstance(body, basestring):
            body = json.loads(body)
        return body, headers


class UpdateableAPIResourceMixin(object):
    def __setitem__(self, k, v):
        self._allow_updates = True
        super(UpdateableAPIResourceMixin, self).__setitem__(k, v)

    def save(self):
        if self._unsaved_values:
            unsaved = self.get_unsaved()
            urlparams, body, headers = self.prepare_to_send('post', **unsaved)
            body, meta = self.session.request('post', self.uri, body, urlparams, headers)
            self.update(unsaved)
            self._unsaved_values = set()
        else:
            logger.debug("Trying to save already saved object %r", self)
        return self

    def get_unsaved(self):
        return dict([(k, getattr(self, k)) for k in self._unsaved_values|set(['id'])])

class ActionResource(Resource):
    def __init__(self, uri, method, cls=None):
        self.uri = uri
        self.method = method
        self.cls = cls

    def post_call(self, session, new_obj=None):
        pass

    def __call__(self, session, **kwargs):
        urlparams, body, headers = self.prepare_to_send(self.method, **kwargs)
        body, meta = session.request(self.method, self.uri, body, urlparams, headers)
        data, meta = self.process_result(body, meta)
        if self.cls:
            new_obj = self.cls.construct_from(session, data, meta)
            self.post_call(session, new_obj)
            return new_obj
        else:
            self.post_call(session)
            return None

class InstanceResource(Resource):
    def __init__(self, session, body=None, meta=None, urlparams=None):
        self._allow_updates = True
        if isinstance(body,dict):
            super(InstanceResource, self).__init__(**body)
        else:
            super(InstanceResource, self).__init__()

        self._unsaved_values = set()

        self._retrieve_params = urlparams
        body = None

        object.__setattr__(self, 'session', session)
        object.__setattr__(self, 'body', body)
        object.__setattr__(self, 'meta', meta)

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(InstanceResource, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError, err:
            raise AttributeError(*err.args)

    def __setitem__(self, k, v):
        if not self._allow_updates:
            raise ValueError("This Eagle Eye Networks object does not allow updates.")

        super(InstanceResource, self).__setitem__(k, v)

        # Allows for unpickling in Python 3.x
        if not hasattr(self, '_unsaved_values'):
            self._unsaved_values = set()

        self._unsaved_values.add(k)

    def __getitem__(self, k):
        return super(InstanceResource, self).__getitem__(k)

    def __delitem__(self, k):
        raise TypeError(
            "You cannot delete attributes on a _EagleeyenetworksObject. ")

    @classmethod
    def construct_from(cls, session, body, meta):
        return cls(session, body, meta)

    @classmethod
    def retrieve(cls, session, **urlparams):
        instance = cls(session, urlparams=urlparams)
        instance.refresh()
        return instance

    def refresh(self):
        body, meta = self.session.request('get', self.uri, urlparams=self._retrieve_params)
        data, meta = self.process_result(body, meta)
        self._unsaved_values = set()
        if isinstance(body, dict):
            self.clear()
            self.update(body)
            body = None
        object.__setattr__(self, 'body', body)
        object.__setattr__(self, 'meta', meta)

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), basestring):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('id'), basestring):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return json.dumps(self, sort_keys=True, indent=2)



