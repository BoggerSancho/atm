from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.base import View


def home(request):
    return render(request, 'cards/card-number.html', {})


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.session.get('number'):
            del self.request.session['number']
        if self.request.session.get('password'):
            del self.request.session['password']
        return HttpResponseRedirect('/')