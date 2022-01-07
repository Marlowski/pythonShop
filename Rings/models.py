from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Ring(models.Model):
    RING_MATERIALS = [
        ('GG', 'Gelbgold'),
        ('WG', 'Weissgold'),
        ('RG', 'Rosegold'),
    ]

    bezeichnung = models.CharField(max_length=100)
    preis = models.DecimalField(max_digits=7, decimal_places=2)
    material = models.CharField(max_length=2, choices=RING_MATERIALS)
    ring_Breite = models.CharField(max_length=5)
    product_img_url = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)

    class Meta:
        ordering = ['bezeichnung', '-preis']
        verbose_name = 'Ring'
        verbose_name_plural = 'Rings'

    def get_full_name(self):
        return_string = self.bezeichnung + ': ' + self.material
        return return_string

    def get_rating(self):
        rating_list = Rating.objects.filter(ring=self)
        average_rating = 0

        if len(rating_list) == 0:
            return average_rating

        for elem in rating_list:
            average_rating += int(elem.rating)

        return round(average_rating / len(rating_list))

    def get_amount_of_ratings(self):
        return len(Rating.objects.filter(ring=self))

    def __str__(self):
        return self.bezeichnung + ' (' + self.material + ')'

    def __repr__(self):
        return self.get_full_name() + ' / ' + str(self.preis) + ' / ' + str(self.ring_Breite)


class Comment(models.Model):
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ring = models.ForeignKey(Ring, on_delete=models.CASCADE)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def get_comment_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def __str__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + ')'

    def __repr__(self):
        return self.get_comment_prefix() + ' (' + self.user.username + ' / ' + str(self.timestamp) + ')'


class Rating(models.Model):
    rating = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ring = models.ForeignKey(Ring, on_delete=models.CASCADE)
