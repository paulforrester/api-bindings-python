from .base import ActionResource, InstanceResource, JsonMixin

class PollResult(InstanceResource):
    pass


class Poll(JsonMixin, ActionResource):
    pass


poll_post = Poll('/poll', 'post', cls=PollResult)
poll_get = Poll('/poll', 'get', cls=PollResult)


def poll(session, cameras=None):
    if cameras:
        return poll_post(session, cameras=cameras)
    else:
        return poll_get(session)