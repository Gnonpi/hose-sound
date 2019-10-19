from rest_framework.reverse import reverse


class TestHoseUserDetail:
    def test_get_own_user(self, login_test_user, client):
        request, user, user_info = login_test_user
        response = client.get(reverse('h:rest_hose_user_detail', kwargs={'pk': user.id}))
        print(response.content.decode('utf8'))
        assert response.status_code == 200
        assert response.content.decode('utf8') == ''
        assert False

    def test_get_other_user(self):
        assert False

    def test_get_non_linked_user(self):
        assert False

    def test_put_new_hoser(self):
        assert False

    def test_delete_non_existing_user(self):
        assert False

    def test_delete_existing_user(self):
        assert False


class TestHoseAssociation:
    def test_(self):
        assert False


class TestHoseContent:
    def test_(self):
        assert False

