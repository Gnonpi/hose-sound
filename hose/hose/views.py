import logging

from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hose_usage.models import HoseUser
from hose_usage.serializers import HoseUserSerializer

logger = logging.getLogger('django')


def legals(request):
    if request.method == 'GET':
        return JsonResponse({'data': {'legal_text': 'I\'ll do it one day'}, 'error': None}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Error getting legal text'}, status=401)


def signup(request):
    logger.debug('Hit the signup')
    username = request.body.json['username']
    if HoseUser.objects.filter(username=username).any():
        return Response({'error': 'Username already used'}, status=status.HTTP_409_CONFLICT)
    email = request.body.json['email']
    if HoseUser.objects.filter(email=email).any():
        return Response({'error': 'Email already used'}, status=status.HTTP_409_CONFLICT)

    serialized = HoseUserSerializer(data=request.DATA)
    if serialized.is_valid():
        HoseUser.objects.create_user(
            username=serialized.init_data['username'],
            email=serialized.init_data['email'],
            password=serialized.init_data['password']
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

