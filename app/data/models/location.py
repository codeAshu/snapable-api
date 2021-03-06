# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Location(models.Model):

    event = models.ForeignKey('Event', help_text='The event this location belongs to.')

    address = models.CharField(max_length=255, help_text='The location address.')
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0, help_text='The address latitude.') # +/- 180.123456, accuracy: 0.111 m (ie. 11.1cm)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0, help_text='The address longitude.') # +/- 180.123456, accuracy: 0.111 m (ie. 11.1cm)

    def __str__(self):
        return u'{0} - ({1},{2})'.format(self.address, self.lat, self.lng)

    def __repr__(self):
        return str({
            'address': self.address,
            'event': self.event,
            'lat': self.lat,
            'lng': self.lng,
        })
