import pytest
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse

from hose_usage.models import HoseUser, HoseAssociation
from hose_usage import views


@pytest.fixture(scope='function')
def my_logged_client(request, django_user_model, client):
    username = 'test_user'
    email = 'test_user@test.com'
    password = 'test_test_test_pwsd'
    user = django_user_model.objects.create(
        username=username,
        email=email,
        password=password
    )
    user.save()
    user_info = {
        'username': username,
        'email': email,
        'password': password,
        'user_id': user.id
    }
    request.addfinalizer(user.delete)
    is_logged = client.login(username=username, password=password)
    print(f'is_logged: {is_logged}')
    client._login(user)
    return request, client, user_info


def test_unauthenticated_user_index(client):
    response = client.get(reverse_lazy('h:home'))
    assert response.status_code == 302


def test_authenticated_user_index(my_logged_client):
    request, client, user_info = my_logged_client
    response = client.get(reverse_lazy('h:home'))
    username = user_info['username']
    assert response.status_code == 200
    assert f'Hi <b>{username}</b>' in response.rendered_content


class TestLinkedHosesView:
    def test_no_hose(self, my_logged_client):
        request, client, user_info = my_logged_client
        user_id = user_info['user_id']
        cnt_has = HoseAssociation.objects. \
            filter(Q(first_end__id=user_id) | Q(second_end__id=user_id)).\
            count()
        assert cnt_has == 0
        client.get(reverse('h:see_hoses'))

    def test_one_hose(self):
        assert False