from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Card


class CardNumberMixin(object):
    def dispatch(self, request, *args, **kwargs):
        number = request.session.get('number')
        if not number:
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)


class CardLoginMixin(object):
    def dispatch(self, request, *args, **kwargs):
        number = request.session.get('number')
        password = request.session.get('password')
        if not number or not password:
            #return HttpResponseForbidden()
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)