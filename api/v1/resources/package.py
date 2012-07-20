from tastypie.resources import ModelResource
from data.models import Package

class PackageResource(ModelResource):
    class Meta:
        queryset = Package.objects.all()
        fields = []
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True