from django.db import models

class ExchangeRates(models.Model):
    date = models.DateTimeField('currency request date')
    currency_request = models.FloatField()

    def __str__(self):
        return f'{self.currency_request}'