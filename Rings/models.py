from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Ring(models.Model):
    RING_MATERIALS = [
        ('G', 'Gold'),
        ('WG', 'Weissgold'),
        ('RG', 'Rosegold'),
    ]

    bezeichnung = models.CharField(max_length=100)

    preis = models.DecimalField(max_digits=7, decimal_places=2)

    material = models.CharField(max_length=2,
                                choices=RING_MATERIALS,
                                )

    ring_Breite = models.CharField(max_length=5)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='users',
                             related_query_name='user',
                             )

    class Meta:
        ordering = ['bezeichnung', '-preis']
        verbose_name = 'Ring'
        verbose_name_plural = 'Rings'

    def get_full_name(self):
        return_string = self.bezeichnung + ': ' + self.material
        return return_string

    def __str__(self):
        return self.bezeichnung + ' (' + self.material + ')'

    def __repr__(self):
        return self.get_full_name() + ' / ' + self.preis + ' / ' + self.ring_Breite
