from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, reverse, get_object_or_404
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from .models import Card, Transaction
from .mixins import CardNumberMixin, CardLoginMixin

# Create your views here.
class CardNumberValidationView(SingleObjectMixin, View):
    model = Card

    def get_object(self):
        # 300seconds = 5minutes | 0 = session cookies will expire when Web browser is closed
        self.request.session.set_expiry(0)
        number = self.request.POST.get('card')
        try:
            card = Card.objects.all().filter(number=number).first()
            return card
        except:
            return None

    def get(self, request):
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        card = self.get_object()
        if not card:
            #messages.error(self.request, 'Incorrect card number or your card is probably blocked!')
            #return HttpResponseRedirect('/')
            message = 'Incorrect card number or your card is probably blocked!'
            return render(request, 'cards/card-error.html', {'message': message})
        request.session['number'] = card.number

        # initialize pin counter for each card
        if not request.session.get(card.number):
            request.session[card.number] = 0
        return HttpResponseRedirect(reverse('cards:pass_validator'))


class CardPasswordValidationView(CardNumberMixin, SingleObjectMixin, View):
    model = Card
    PIN_LIMIT = 3

    def lock_card(self):
        number = self.request.session.get('number')
        card = Card.objects.all().filter(number=number).first()
        card.locked = True
        card.save()
        del self.request.session['number']
        del self.request.session[number]

    def get_object(self):
        number = self.request.session.get('number')
        password = self.request.POST.get('pass')
        try:
            card = Card.objects.all().filter(number=number, password=password).first()
            return card
        except:
            return None

    def get(self, request):
        return render(request, 'cards/card-password.html', {})

    def post(self, request):
        card_number = request.session.get('number')
        card = self.get_object()
        if card:
            request.session['password'] = True
            request.session[card_number] = 0
            return HttpResponseRedirect(reverse('cards:menu'))
        pin_invalid_counter = request.session.get(card_number)
        pin_invalid_counter += 1
        request.session[card_number] = pin_invalid_counter
        message = 'Wrong password!'
        if pin_invalid_counter > self.PIN_LIMIT:
            self.lock_card()
            message = 'Your card is blocked!'
        return render(request, 'cards/card-error.html', {'message':message})


class CardOperationsView(CardLoginMixin, SingleObjectMixin, View):
    model = Card
    template_name = 'cards/card-operations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class CardDetailView(CardLoginMixin, SingleObjectMixin, View):
    model = Card
    template_name = 'cards/card-detail.html'

    def get_object(self, queryset=None):
        card_number = self.request.session.get('number')
        object = get_object_or_404(Card, number=card_number)
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request):
        self.object = self.get_object()
        context = self.get_context_data()
        transaction = Transaction()
        transaction.card = self.object
        transaction.type = 'balance'
        transaction.save()
        return render(request, self.template_name, context)


class CardWithdrawalView(CardLoginMixin, SingleObjectMixin, View):
    model = Card
    template_name = 'cards/card-withdrawal.html'

    def get_object(self, queryset=None):
        card_number = self.request.session.get('number')
        object = get_object_or_404(Card, number=card_number)
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request):
        self.object = self.get_object()
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        self.object = self.get_object()
        context = self.get_context_data()
        required_cash = int(request.POST.get('cash'))
        current_cash = self.object.balance
        if required_cash < current_cash:
            transaction = Transaction()
            transaction.card = self.object
            transaction.type = 'withdrawal'
            transaction.cash_value = required_cash
            transaction.save()
            return HttpResponseRedirect(reverse('cards:checkout'))

        #messages.error(self.request, 'Not enough money on your card!')
        #return render(request, self.template_name, context)
        message = 'Not enough money on your card!'
        return render(request, 'cards/card-error.html', {'message': message})


class CardCheckoutView(CardLoginMixin, SingleObjectMixin, View):
    template_name = 'cards/card-checkout.html'
    model = Transaction

    def get_object(self, *args, **kwargs):
        card_number = self.request.session.get('number')
        card = get_object_or_404(Card, number=card_number)
        transaction = card.transaction_set.all().order_by('-pk').first()
        return transaction

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request):
        self.object = self.get_object()
        context = self.get_context_data()
        return render(request, self.template_name, context)