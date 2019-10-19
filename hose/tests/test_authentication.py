import json

from django.urls import reverse

from hose_usage.models import HoseUser

JSON_HEADER = 'application/json'


class TestSignup:
    def test_wrong_payload(self, client):
        wrong_payload = {
            'cacao': 'chocolat'
        }
        response = client.post(reverse('signup'), wrong_payload, content_type=JSON_HEADER)
        assert response.status_code == 400
        assert 'Wrong payload' in response.content.decode('utf8')

    def test_already_exist_username(self, client, create_test_user):
        user, user_info = create_test_user
        already_username_payload = {
            'username': user_info['username'],
            'email': user_info['email'] + 'o',
            'password': user_info['password'] + 'o'
        }
        response = client.post(reverse('signup'), already_username_payload, content_type=JSON_HEADER)
        assert response.status_code == 409
        assert 'Username already used' in response.content.decode('utf8')

    def test_already_exist_email(self, client, create_test_user):
        user, user_info = create_test_user
        already_email_payload = {
            'username': user_info['username'] + 'o',
            'email': user_info['email'],
            'password': user_info['password'] + 'o'
        }
        response = client.post(reverse('signup'), already_email_payload, content_type=JSON_HEADER)
        assert response.status_code == 409
        assert 'Email already used' in response.content.decode('utf8')

    def test_not_serializable(self, client, create_test_user):
        user, user_info = create_test_user
        already_not_serializable = {
            'username': {
                'display': user_info['username'],
                'name': user_info['username']
            },
            'email': user_info['email'] + 'o',
            'password': user_info['password'] + 'o'
        }
        response = client.post(reverse('signup'), already_not_serializable, content_type=JSON_HEADER)
        assert response.status_code == 400
        assert 'Not a valid string' in response.content.decode('utf8')

    def test_valid_register(self, client, db):
        user_info = {
            'username': 'test-new-user',
            'email': 'test-new-email',
            'password': 'test-new-password',
        }
        response = client.post(reverse('signup'), user_info, content_type=JSON_HEADER)
        assert response.status_code == 201
        username = user_info['username']
        assert f'User {username} was created' in response.content.decode('utf8')
        created_user = HoseUser.objects.filter(
            username=username,
            email=user_info['email'],
        ).first()
        assert created_user is not None
        assert created_user.username == username
        assert created_user.email == user_info['email']


class TestObtainToken:
    def test_wrong_payload(self, client):
        response = client.post(reverse('obtain_jwt'), {'cacao': 'chocolat'})
        assert response.status_code == 400
        assert 'This field is required' in response.content.decode('utf8')

    def test_not_exist_user(self, client, db):
        test_none_user = 'Francis'
        user = HoseUser.objects.filter(username=test_none_user).all()
        assert len(user) == 0
        response = client.post(reverse('obtain_jwt'),
                               {'username': test_none_user, 'password': 'ajax'})
        assert response.status_code == 400
        assert 'Unable to log in with provided credentials.' in response.content.decode('utf8')

    def test_valid_login(self, client, create_test_user):
        user, user_info = create_test_user
        response = client.post(
            reverse('obtain_jwt'),
            {'username': user_info['username'], 'password': user_info['password']}
        )
        print(response.status_code)
        print(response.content)
        assert False

#
# class TestRefreshToken:
#     def test_(self):
#         assert False
#
#
# class TestVerifyToken:
#     def test_(self):
#         assert False

