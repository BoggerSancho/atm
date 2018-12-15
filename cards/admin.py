from django.contrib import admin

# Register your models here.
from .models import Card, Transaction

admin.site.register(Card)
admin.site.register(Transaction)