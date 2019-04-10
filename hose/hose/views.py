import django
from rest_framework import status
from django.http import JsonResponse


def legals(request):
    if request.method == 'GET':
        return JsonResponse({'data': {'legal_text': 'I\'ll do it one day'}, 'error': None}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Error getting legal text'}, status=401)
