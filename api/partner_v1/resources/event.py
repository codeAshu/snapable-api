import api.auth
import api.base_v1.resources
import pytz

from datetime import datetime, timedelta
from decimal import Decimal

from django.conf.urls.defaults import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.http import HttpResponse, Http404

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ALL

from account import AccountResource

from data.models import Address
from data.models import Event
from data.models import Photo
from data.models import User

from api.utils import EventSerializer

class EventResource(api.base_v1.resources.EventResource):

    # relations
    account = fields.ForeignKey(AccountResource, 'account', help_text='Account resource')
    addresses = fields.ToManyField('api.partner_v1.resources.AddressResource', 'address_set', null=True, full=True) 

    # virtual fields
    photo_count = fields.IntegerField(attribute='photo_count', readonly=True, help_text='The number of photos for the event.')

    Meta = api.base_v1.resources.EventResource.Meta
    Meta.fields += ['photo_count']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.DatabaseAuthentication()
    Meta.authorization = api.auth.DatabaseAuthorization()
    Meta.serializer = EventSerializer(formats=['json', 'jpeg'])
    Meta.filtering = dict(Meta.filtering, **{
        'enabled': ['exact'],
        'account': ['exact'],
        'start': ALL,
        'end': ALL,
        'title': ALL,
        'url': ALL,
        'q': ['exact'],
    })

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

    # override the response
    def create_response(self, request, bundle, response_class=HttpResponse, **response_kwargs):
        """
        Override the default create_response method.
        """
        if (request.META['REQUEST_METHOD'] == 'GET' and request.GET.has_key('size')):
            bundle.data['size'] = request.GET['size']

        return super(EventResource, self).create_response(request, bundle, response_class=response_class, **response_kwargs)