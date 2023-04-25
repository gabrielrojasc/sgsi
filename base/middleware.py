# standard imports

import threading


class RequestMiddleware:
    """
    Middleware that stores the user that made a request. This is used when logging
    object creations/updates/deletions to obtain the user performing such action.
    """

    thread_local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Save the user that makes the request
        self.thread_local.user = request.user
        return self.get_response(request)
