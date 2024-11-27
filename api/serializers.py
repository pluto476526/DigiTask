from rest_framework.serializers import ModelSerializer
from dash.models import Job_Listing



class JobSerializer(ModelSerializer):
    class Meta:
        model = Job_Listing
        fields = '__all__'


