from django.http import HttpResponseBadRequest
import functools


def ajax_required(f):
    @functools.wraps(f)
    def wrap(request, *args, **kw):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kw)
    return wrap
