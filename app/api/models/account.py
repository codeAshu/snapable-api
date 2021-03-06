# django/tastypie/libs
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ApiAccount(models.Model):

    email = models.EmailField(help_text='The email contact for the API.')
    company = models.CharField(max_length=255, null=True, help_text='The name of the organization or company.')
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the api account was created. (UTC)')

    def __str__(self):
        return '{0}'.format(self.company)

    def __repr__(self):
        return str({
            'email': self.email,
            'company': self.company,
            'created_at': self.created_at,
            'pk': self.pk,
        })
