from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4


class Token(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                             verbose_name='User', related_name='registration_token')
    token=models.UUIDField(verbose_name='token', default=uuid4)

    def __str__(self):
        return str(self.token)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, verbose_name='User')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Avatar')
    about_user = models.TextField(max_length=2000, null=True, blank=True, verbose_name='About User')
    github = models.URLField(null=True, blank=True, verbose_name='GitHub')


    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


