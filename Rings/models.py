import locale
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Ring(models.Model):
    RING_MATERIALS = [
        ('GG', 'Gelbgold'),
        ('WG', 'Weissgold'),
        ('RG', 'Rosegold'),
    ]

    bezeichnung = models.CharField(max_length=100)
    preis = models.DecimalField(max_digits=7, decimal_places=2)
    material = models.CharField(max_length=2, choices=RING_MATERIALS)
    category = models.CharField(max_length=100)
    ring_size = models.CharField(max_length=5)
    product_img_url = models.ImageField(upload_to='product_images/', blank=True, null=True)
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

    def get_rating_objects(self):
        return Rating.objects.filter(ring=self)

    def get_formatted_categorys(self):
        cat_string = self.category
        return cat_string.replace("|", ", ")

    def __str__(self):
        return self.bezeichnung + ' (' + self.get_material_display() + ')'

    def __repr__(self):
        return self.get_full_name() + ' / ' + str(self.preis) + ' / ' + str(self.ring_size)


class Rating(models.Model):
    rating = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ring = models.ForeignKey(Ring, on_delete=models.CASCADE)
    comment = models.CharField(max_length=2500)

    def get_formatted_date(self):
        locale.setlocale(locale.LC_ALL, 'de_DE')
        return self.timestamp.strftime("%d. %B, %Y")

    def get_pos_evaluation_amount(self):
        return len(RatingEvaluation.objects.filter(rating=self.id, evaluation="POS"))

    def get_neg_evaluation_amount(self):
        return len(RatingEvaluation.objects.filter(rating=self.id, evaluation="NEG"))

    def get_rep_evaluation_amount(self):
        return len(RatingEvaluation.objects.filter(rating=self.id, evaluation="REP"))


class RatingEvaluation(models.Model):
    EVALUATION = [
        ('POS', 'helpful'),
        ('NEG', 'not helpful'),
        ('REP', 'reported')
    ]
    evaluation = models.CharField(max_length=3, choices=EVALUATION)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
