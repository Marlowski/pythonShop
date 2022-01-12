from django.contrib.auth.models import AbstractUser
from django.db import models


# thats like 10% of the implementation, just for cart settings to work at the moments
class MyUser(AbstractUser):
    pass

    profile_picture = models.ImageField(upload_to='picture_uploads/', blank=True, null=True)

    def __str__(self):
        return self.username + " - (" + self.email + ")"
