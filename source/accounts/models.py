from django.db import models
from uuid import uuid4


class Token(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             verbose_name='user', related_name='registration_token')
    token=models.UUIDField(verbose_name='token', default=uuid4)

    def __str__(self):
        return str(self.token)
