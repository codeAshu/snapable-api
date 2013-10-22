import api.auth
import api.utils
import api.base_v1.resources
import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ALL
from tastypie.utils.mime import determine_format, build_content_type

from event import EventResource
from guest import GuestResource

from data.models import Guest

from api.utils.serializers import SnapSerializer

from data.images import SnapImage
import cStringIO
from PIL import Image

class PhotoResource(api.utils.MultipartResource, api.base_v1.resources.PhotoResource):

    event = fields.ForeignKey(EventResource, 'event')
    guest = fields.ForeignKey(GuestResource, 'guest', null=True) # allow the foreign key to be null

    created_at = fields.DateTimeField(attribute='created_at', readonly=True, help_text='The photo timestamp. (UTC)')

    class Meta(api.base_v1.resources.PhotoResource.Meta): # set Meta to the public API Meta
        fields = api.base_v1.resources.PhotoResource.Meta.fields + ['metrics'];
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()
        serializer = SnapSerializer(formats=['json', 'jpeg'])
        filtering = dict(api.base_v1.resources.PhotoResource.Meta.filtering, **{
            'event': ['exact'],
            'streamable': ['exact'],
            'created_at': ALL,
        })

    def dehydrate(self, bundle):

        # try and add the guest name
        try:
            # add the guest name as the photo name
            bundle.data['author_name'] = bundle.obj.guest.name
        except AttributeError:
            bundle.data['author_name'] = ''

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['type'] = '/private_v1/type/6/'
        bundle.data['timestamp'] = bundle.data['created_at'].strftime('%Y-%m-%dT%H:%M:%S')

        return bundle

    def hydrate(self, bundle):
        # required
        if 'event' in bundle.data:
            bundle.obj.event_id = bundle.data['event']
        if 'guest' in bundle.data:
            bundle.obj.guest_id = bundle.data['guest']

        return bundle

    def obj_create(self, bundle, **kwargs):
        try:
            # make sure the image is in the request
            img = Image.open(cStringIO.StringIO(bundle.data['image'].read()))
            snapimg = SnapImage(img)
        except KeyError as key:
            raise BadRequest('Missing field: ' + str(key))

        bundle = super(PhotoResource, self).obj_create(bundle, **kwargs)
        photo = bundle.obj

        # set the value of the event streamable value
        photo.streamable = photo.event.are_photos_streamable
        photo.save()

        # try and watermark
        if photo.event.are_photos_watermarked == True:
            try:
                # save the image to cloudfiles
                watermark = photo.event.get_watermark()
                photo.save_image(snapimg, True, watermark=watermark)

            except Exception as e:
                # save the image to cloudfiles
                photo.save_image(snapimg, True)

        else:
            # save the image to cloudfiles
            photo.save_image(snapimg, True)

        return bundle