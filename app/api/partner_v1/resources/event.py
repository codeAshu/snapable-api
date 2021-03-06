# python
import re

# django/tastypie/libs
from django.db.models import Q
from tastypie import fields
from tastypie.resources import ALL
from tastypie.validation import Validation

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Account, Event, Guest, Location, Photo, User

class EventValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        required = ['account', 'end_at', 'start_at', 'title', 'url']
        for key in required:
            try:
                bundle.data[key]
            except KeyError:
                errors[key] = 'Missing field'

        # check the url
        url_str = bundle.data['url']
        if len(url_str) < 6:
            errors['url'] = 'Event url is too short. Must be at least 6 characters.'
        if re.search('[^a-zA-Z0-9-_]', url_str) is not None:
            errors['url'] = 'Invalid url characters. Only allowed: [a-zA-Z0-9-_]'
        if (request.method not in ['PUT', 'PATCH']) and Event.objects.filter(url=url_str).count() > 0:
            errors['url'] = 'An event with that url already exists.'
        if (request.method in ['PUT', 'PATCH']) and Event.objects.filter(~Q(pk=bundle.data['pk']) & Q(url=url_str)).count() > 0:
            errors['url'] = 'An event with that url already exists.'

        for key, value in bundle.data.items():
            # if the addresses field is set
            if key == 'locations':
                # check the outer item
                errors[key] = "Cannot create endpoints via the event. Use the 'location' endpoint."
                # check the inner item

        return errors

class EventResource(BaseModelResource):

    # relations
    account = fields.ForeignKey('api.partner_v1.resources.AccountResource', 'account', help_text='Account resource')
    locations = fields.ToManyField('api.partner_v1.resources.LocationResource', 'location_set', null=True, full=True) 

    # virtual fields
    photo_count = fields.IntegerField(attribute='photo_count', readonly=True, help_text='The number of photos for the event.')

    class Meta(BaseMeta):
        queryset = Event.objects.all()
        fields = ['start_at', 'end_at', 'tz_offset', 'title', 'url', 'pin', 'is_enabled', 'is_public', 'photo_count']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        validation = EventValidation()
        filtering = {
            'is_enabled': ['exact'],
            'account': ['exact'],
            'start_at': ALL,
            'end_at': ALL,
            'title': ALL,
            'url': ALL,
            'q': ['exact'],
        }

    def dehydrate_end_at(self, bundle):
        return bundle.data['end_at'].strftime('%Y-%m-%dT%H:%M:%SZ')

    def dehydrate_start_at(self, bundle):
        return bundle.data['start_at'].strftime('%Y-%m-%dT%H:%M:%SZ')

    def obj_create(self, bundle, **kwargs):
        bundle = super(EventResource, self).obj_create(bundle, **kwargs)

        # create a new guest
        user = bundle.obj.account.users.all()[0]
        guest = Guest(event=bundle.obj, email=user.email, name=user.name)
        guest.save()

        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        
        orm_filters = super(EventResource, self).build_filters(filters)

        if 'q' in filters:
            qset = (
                (Q(title__icontains=filters['q']) | Q(url__icontains=filters['q']))
            )
        
            orm_filters.update({'q': qset})

        return orm_filters


    def apply_filters(self, request, applicable_filters):
        # some local variables
        custom_filters = []
        custom_virtual_filters = dict()

        # queryset filters
        if 'q' in applicable_filters:
            custom_filters.append(applicable_filters.pop('q'))

        # inital filtering
        semi_filtered = super(EventResource, self).apply_filters(request, applicable_filters)

        # do our queryset filtering
        for custom_filter in custom_filters:
            semi_filtered = semi_filtered.filter(custom_filter)
        
        return semi_filtered
