from django.db import models

from data.models import Account
from data.models import Addon

class Event(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    account = models.ForeignKey(Account)
    addons = models.ManyToManyField(Addon, through='EventAddon')

    cover = models.IntegerField(default=0, help_text='Integer data. The photo ID of the image to use for the event cover.') # dirty hack... fix this...

    start = models.DateTimeField(help_text='Event start time. (UTC)')
    end = models.DateTimeField(help_text='Event end time. (UTC)')
    tz_offset = models.IntegerField(default=0, help_text='The timezone offset (in minutes) from UTC.')
    title = models.CharField(max_length=255, help_text='Event title.')
    url = models.CharField(max_length=255, help_text='A "short name" for the event.')
    public = models.BooleanField(default=True, help_text='Is the event considered "public".')
    pin = models.CharField(max_length=255, help_text='Pseudo-random PIN used for private events.')
    creation_date = models.DateTimeField(auto_now_add=True, help_text='When the event created. (UTC)')
    last_access = models.DateTimeField(auto_now_add=True, help_text='When the event was last accessed. (UTC)')
    access_count = models.IntegerField(default=0)
    enabled = models.BooleanField(help_text='Is the event considered "active" in the system.')

    # return the number of photos related to this event
    def _get_photo_count(self):
        return self.photo_set.count()

    def _set_photo_count(self):
        pass

    photo_count = property(_get_photo_count, _set_photo_count)