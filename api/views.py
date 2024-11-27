from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dash.models import Job_Listing
from api.serializers import JobSerializer

# Create your views here.

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/entries',
        'GET /api/entries/:id',
    ]
    return Response(routes)


@api_view(['GET'])
def get_entries(request):
    entries = Job_Listing.objects.filter(status='posted')
    serializer = JobSerializer(entries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_entry(request, pk):
    entry = get_object_or_404(Job_Listing, id=pk)
    serializer = JobSerializer(entry, many=False)
    return Response(serializer.data)
