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

    material = models.CharField(max_length=2,
                                choices=RING_MATERIALS,
                                )

    ring_Breite = models.CharField(max_length=5)

    product_img_url = models.CharField(max_length=300)

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

    def get_upvotes(self):
        upvotes = Vote.objects.filter(up_or_down='U',
                                      ring=self)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Vote.objects.filter(up_or_down='D',
                                        ring=self)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def get_average_upvote(self):
        if len(self.get_upvotes()) != 0:
            # return % value
            return round(len(self.get_upvotes())/(len(self.get_upvotes()) + len(self.get_downvotes())) * 100)
        else:
            # only downvotes
            if len(self.get_downvotes()) != 0:
                return 0
            # no votes yet
            else:
                return None

    def vote(self, user, up_or_down):
        u_or_d = 'U'
        if up_or_down == 'down':
            u_or_d = 'D'
        vote = Vote.objects.create(up_or_down=u_or_d,
                                   user=user,
                                   ring=self
                                   )

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


class Vote(models.Model):
    VOTE_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]

    up_or_down = models.CharField(max_length=1,
                                  choices=VOTE_TYPES,
                                  )
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ring = models.ForeignKey(Ring, on_delete=models.CASCADE)

    def __str__(self):
        return self.up_or_down + ' on ' + self.ring.bezeichnung + ' by ' + self.user.username
