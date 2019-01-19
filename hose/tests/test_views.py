import pytest
from django.urls import reverse_lazy

from hose_usage.models import HoseUser


# @pytest.fixture(scope='function')
# def create_test_user(request):
#     tmp_user = HoseUser.objects.create_user(
#         username='test_user',
#         email='test@test.com',
#         password='test_test_test_pwsd'
#     )
#     yield tmp_user
#     request.addfinalizer(tmp_user.delete)
from hose_usage.views import HomeView


def test_unauthenticated_user_index(django_user_model, client):
    response = client.get(reverse_lazy('h:home'))
    assert response.status_code == 200
    assert False


def test_authenticated_user_index(request, django_user_model, client):
    username = 'test_user'
    email = 'test_user@test.com'
    password = 'test_test_test_pwsd'
    user = django_user_model.objects.create(
        username=username,
        email=email,
        password=password
    )
    user.save()
    request.addfinalizer(user.delete)
    client.login(username=username, password=password)
    response = client.get(reverse_lazy('h:home'))
    assert response.status_code == 200
    assert f'Hi {username}' in response.rendered_content

