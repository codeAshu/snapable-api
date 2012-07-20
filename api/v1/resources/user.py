from tastypie.constants import ALL
from tastypie.resources import ModelResource
from data.models import User

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        fields = ['email', 'first_name', 'last_name']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
            "email": ALL,
        }