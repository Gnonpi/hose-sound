import pytest

from hose_core.models import Base, engine
from hose_core.base_operation import create_hoseuser, create_hose
from hose_core.models import Session, HoseUser, Hose


@pytest.fixture(scope='class')
def create_tables(request):
    import os
    print(f"APP_ENV: {os.environ.get('APP_ENV')}")
    print(f'engine: {engine}')
    Base.metadata.create_all(engine)
    yield
    Base.metadata.clear()


@pytest.mark.usefixtures('create_tables')
class TestCreateHoseUser:

    @pytest.fixture(autouse=True)
    def clean_users(self):
        session = Session()
        session.query(HoseUser).delete()
        session.commit()
        session.close()

    def test_create_user(self):
        id_user = create_hoseuser('test-user', 'test@test.com', 'hashedp')

        session = Session()
        list_users = session.query(HoseUser).filter_by(name='test-user').all()
        assert len(list_users) == 1
        one_user = list_users[0]
        assert one_user.id_user == id_user
        assert one_user.name == 'test-user'
        assert one_user.email == 'test@test.com'
        session.close()

    def test_create_existing_name(self):
        username = 'test-user-repeated'
        id_user_first = create_hoseuser(username, 'test-first@test.com', 'hashedp')
        id_user_second = create_hoseuser(username, 'test-second@test.com', 'hashedpwd')

        session = Session()
        list_users = session.query(HoseUser).filter_by(name=username).all()
        assert len(list_users) == 1
        one_user = list_users[0]
        assert one_user.id_user == id_user_first
        assert one_user.name == username
        assert one_user.email == 'test-first@test.com'
        session.close()


@pytest.mark.usefixtures('create_tables')
class TestCreateHose:
    @pytest.fixture(autouse=True)
    def clean_tables(self):
        session = Session()
        session.query(Hose).delete()
        session.query(HoseUser).delete()
        session.commit()
        session.close()

    def test_create_hose(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')

        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').first()
        user_b = session.query(HoseUser).filter_by(name='user-b').first()
        id_hose = create_hose(user_a, user_b)
        list_hose = session.query(Hose).filter_by(id_user_a=user_a.id_user, id_user_b=user_b.id_user).all()

        assert len(list_hose) == 1
        one_hose = list_hose[0]
        assert one_hose.id_user_a == id_user_a
        assert one_hose.id_user_b == id_user_b
        assert one_hose.id_hose == id_hose
        session.close()
