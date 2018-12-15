import hashlib

from django.db import models
from django.db.models.signals import post_save, pre_save

# Create your models here.
class CardQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(locked=False)


class CardManager(models.Manager):
    def get_queryset(self):
        return CardQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()


class Card(models.Model):
    number = models.TextField(max_length=16, unique=True)
    password = models.TextField(max_length=256)
    locked = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)

    objects = CardManager()

    def __str__(self):
        return self.number


def card_item_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        password = instance.password
        password = hashlib.md5(password.encode())
        instance.password = password.hexdigest()
        instance.save()

post_save.connect(card_item_post_save_receiver, sender=Card)


TRANSACTION_TYPE_CHOICES = (
    ('balance', 'Balance'),
    ('withdrawal', 'Withdrawal'),
)

class Transaction(models.Model):
    card        = models.ForeignKey(Card, on_delete=models.CASCADE)
    type        = models.CharField(max_length=120, choices=TRANSACTION_TYPE_CHOICES)
    timestamp   = models.DateTimeField(auto_now_add=True, auto_now=False)
    cash_value  = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.card}:{self.type}:{self.timestamp}'


def transaction_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.type == 'balance':
        instance.cash_value = instance.card.balance
    if instance.type == 'withdrawal':
        instance.card.balance -= instance.cash_value
        instance.card.save()

pre_save.connect(transaction_pre_save_receiver, sender=Transaction)