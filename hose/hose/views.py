import json
import logging

from rest_framework import status
from django.http import JsonResponse

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
    if request.method != 'POST':
        return JsonResponse({'error': 'Wrong method to signup, expect POST'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    json_body = json.loads(request.body)

    # todo: start using json_schema
    if set(json_body) != {'username', 'email', 'password'}:
        return JsonResponse({'error': 'Wrong payload, expecting username+email+password'}, status=status.HTTP_400_BAD_REQUEST)

    username = json_body['username']
    email = json_body['email']
    if HoseUser.objects.filter(username=username).first():
        return JsonResponse({'error': 'Username already used'}, status=status.HTTP_409_CONFLICT)
    if HoseUser.objects.filter(email=email).first():
        return JsonResponse({'error': 'Email already used'}, status=status.HTTP_409_CONFLICT)

    serialized = HoseUserSerializer(data=json_body)
    if serialized.is_valid():
        HoseUser.objects.create_user(
            username=json_body['username'],
            email=json_body['email'],
            password=json_body['password']
        )
        return JsonResponse({'data': f'User {username} was created'}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
