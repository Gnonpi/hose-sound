import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def create_test_user(request, django_user_model):
    user_info = {
        'username': 'test_user',
        'email': 'test_user@test.com',
        'password': 'test_test_test_pwsd',
        'user_id': None,
    }
    user = django_user_model.objects.create(
        username=user_info['username'],
        email=user_info['email'],
        password=user_info['password']
    )
    user.save()
    logger.debug('User saved')
    user_info['user_id'] = user.id
    request.addfinalizer(user.delete)

    return user, user_info


@pytest.fixture(scope='function')
def login_test_user(request, create_test_user, client):
    user, user_info = create_test_user
    is_logged = client.login(username=user_info['username'], password=user_info['password'])
    if is_logged is False:
        raise RuntimeError(f'Could not login {user_info}')
    logger.debug('User logged in')
    client._login(user)
    return request, client, user_info
