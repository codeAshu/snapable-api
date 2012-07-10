from django.db import models
from api.data.models.event import Event

class Address(models.Model):
    
    class Meta:
        app_label = 'data'

    event = models.ForeignKey(Event)
    address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=9, decimal_places=6) # +/- 180.123456, accuracy: 0.111 m (ie. 11.1cm)
    lng = models.DecimalField(max_digits=9, decimal_places=6) # +/- 180.123456, accuracy: 0.111 m (ie. 11.1cm)
    creation_date = models.DateTimeField(auto_now_add=True)