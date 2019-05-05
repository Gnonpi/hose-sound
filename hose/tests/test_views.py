import pytest
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.test import Client
from django.urls import reverse_lazy, reverse

from hose_usage.models import HoseUser, HoseAssociation, AssociationDemand

#
# @pytest.fixture(scope='function')
# def my_logged_client(request, django_user_model, client):
#     username = 'test_user'
#     email = 'test_user@test.com'
#     password = 'test_test_test_pwsd'
#     user = django_user_model.objects.create(
#         username=username,
#         email=email,
#         password=password
#     )
#     user.save()
#     user_info = {
#         'username': username,
#         'email': email,
#         'password': password,
#         'user_id': user.id,
#     }
#     request.addfinalizer(user.delete)
#     is_logged = client.login(username=username, password=password)
#     print(f'is_logged: {is_logged}')
#     client._login(user)
#     return request, client, user_info


def test_unauthenticated_user_index(client):
    response = client.get(reverse_lazy('home'))
    assert response.status_code == 302


def test_authenticated_user_index(my_logged_client):
    cl_request, client, user_info = my_logged_client
    response = client.get(reverse_lazy('h:home'))
    username = user_info['username']
    assert response.status_code == 200
    assert f'Hi <b>{username}</b>' in response.rendered_content


class TestLinkedHosesView:
    def test_no_hose(self, my_logged_client):
        cl_request, client, user_info = my_logged_client
        user_id = user_info['user_id']
        cnt_has = HoseAssociation.objects. \
            filter(Q(first_end__id=user_id) | Q(second_end__id=user_id)).\
            count()
        assert cnt_has == 0
        message_no_hose = "No hoses are available."
        response = client.get(reverse('h:see_hoses'))
        assert response.status_code == 200
        assert message_no_hose in response.rendered_content

    def test_one_hose(self, request, my_logged_client):
        cl_request, client, user_info = my_logged_client
        user_id = user_info['user_id']
        user = get_object_or_404(HoseUser, pk=user_id)
        other_username = 'other_test_user'
        hose_name = 'test_hose'
        other_user = HoseUser(username=other_username, email='test@gmail.com', password='test_test_test')
        other_user.save()
        request.addfinalizer(other_user.delete)
        ha = HoseAssociation(hose_name=hose_name, first_end=user, second_end=other_user)
        ha.save()
        response = client.get(reverse('h:see_hoses'))
        assert response.status_code == 200
        assert hose_name in response.rendered_content
        response = client.get(reverse('h:show_hose', kwargs={'hose_id': ha.id}))
        assert response.status_code == 200
        assert hose_name in response.content.decode('utf-8')


class TestInviteSystem:
    def test_normal_usage(self, request, my_logged_client):
        cl_request, client, user_info = my_logged_client
        user_id = user_info['user_id']
        user = get_object_or_404(HoseUser, pk=user_id)
        other_username = 'other_test_user'
        other_pwsd = 'test_test_test'
        cnt_other_user = HoseUser.objects.filter(username=other_username).count()
        assert cnt_other_user == 0
        other_user = HoseUser(username=other_username, email='test@gmail.com', password=other_pwsd)
        other_user.save()
        request.addfinalizer(other_user.delete)

        # make demand
        response = client.get(reverse('h:hoser_ask', kwargs={'hoser_id': other_user.id}))
        assert response.status_code == 200
        demand = AssociationDemand.objects.filter(sender=user, receiver=other_user).first()
        assert demand is not None
        # confirm demand
        c = Client()
        c.get('/login/', {'username': other_username, 'password': other_pwsd})
        response = c.get(reverse('h:hoser_confirm', kwargs={'demand_id': demand.id}))
        assert response.status_code == 200

        ha = HoseAssociation.objects.filter(first_end__id=user.id, second_user__id=other_user.id).first()
        assert ha is not None

