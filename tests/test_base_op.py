import pytest

from hose_core.exceptions import UserNotBelongingToHoseError
from hose_core.models import Session, HoseUser, Hose, Content, ContentType
from hose_core.models import Base, engine
from hose_core.base_operation import create_hoseuser, create_hose, add_content, get_hose_between_user


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
        session.query(Content).delete()
        session.query(ContentType).delete()
        session.query(Hose).delete()
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
        session.query(Content).delete()
        session.query(ContentType).delete()
        session.query(Hose).delete()
        session.query(HoseUser).delete()
        session.commit()
        session.close()

    def test_switch_id_user(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')

        assert id_user_a < id_user_b
        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').one()
        user_b = session.query(HoseUser).filter_by(name='user-b').one()
        id_hose = create_hose(user_b, user_a)
        list_hose = session.query(Hose).filter_by(id_user_a=user_a.id_user, id_user_b=user_b.id_user).all()
        assert len(list_hose) == 1
        one_hose = list_hose[0]
        assert one_hose.id_hose == id_hose
        assert one_hose.id_user_a == id_user_a
        assert one_hose.id_user_b == id_user_b

    def test_create_hose(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')

        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').one()
        user_b = session.query(HoseUser).filter_by(name='user-b').one()
        id_hose = create_hose(user_a, user_b)
        list_hose = session.query(Hose).filter_by(id_user_a=user_a.id_user, id_user_b=user_b.id_user).all()

        assert len(list_hose) == 1
        one_hose = list_hose[0]
        assert one_hose.id_user_a == id_user_a
        assert one_hose.id_user_b == id_user_b
        assert one_hose.id_hose == id_hose
        session.close()


@pytest.mark.usefixtures('create_tables')
class TestGetHoseBetweenUsers:
    @pytest.fixture(autouse=True)
    def clean_tables(self):
        session = Session()
        session.query(Content).delete()
        session.query(ContentType).delete()
        session.query(Hose).delete()
        session.query(HoseUser).delete()
        session.commit()
        session.close()

    def test_no_hose_between_users(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')
        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').one()
        user_b = session.query(HoseUser).filter_by(name='user-b').one()
        id_hose = get_hose_between_user(user_a, user_b)
        assert id_hose is None

    def test_hose_only_one_user(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')
        id_user_c = create_hoseuser('user-c', 'test-c@test.com', 'hashedpsswd')
        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').one()
        user_b = session.query(HoseUser).filter_by(name='user-b').one()
        user_c = session.query(HoseUser).filter_by(name='user-c').one()
        id_hose_ac = create_hose(user_a, user_c)
        id_hose_ab = get_hose_between_user(user_a, user_b)
        assert id_hose_ab is None

    def test_user_wrong_order(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')
        assert id_user_a < id_user_b
        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').one()
        user_b = session.query(HoseUser).filter_by(name='user-b').one()
        id_hose_db = create_hose(user_a, user_b)
        id_hose_get = get_hose_between_user(user_b, user_a)
        assert id_hose_db == id_hose_get

    def test_get_hose_between_users(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')
        assert id_user_a < id_user_b
        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').one()
        user_b = session.query(HoseUser).filter_by(name='user-b').one()
        id_hose_db = create_hose(user_a, user_b)
        id_hose_get = get_hose_between_user(user_a, user_b)
        assert id_hose_db == id_hose_get


@pytest.mark.usefixtures('create_tables')
class TestCreateContent:
    @pytest.fixture(autouse=True)
    def clean_tables(self):
        session = Session()
        session.query(Content).delete()
        session.query(ContentType).delete()
        session.query(Hose).delete()
        session.query(HoseUser).delete()
        session.commit()
        session.close()

    def test_wrong_user_adding(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')
        id_user_c = create_hoseuser('user-c', 'test-c@test.com', 'hashedpsswd')

        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').one()
        user_b = session.query(HoseUser).filter_by(name='user-b').one()
        user_c = session.query(HoseUser).filter_by(name='user-c').one()
        id_hose = create_hose(user_a, user_b)
        hose = session.query(Hose).filter_by(id_hose=id_hose).one()

        with pytest.raises(UserNotBelongingToHoseError) as ex:
            id_content = add_content(user_c, hose, 'path', 'youtube-link')

    def test_create_content_type_if_needed(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')
        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').one()
        user_b = session.query(HoseUser).filter_by(name='user-b').one()
        id_hose = create_hose(user_a, user_b)
        hose = session.query(Hose).filter_by(id_hose=id_hose).one()

        existing_content_types = session.query(ContentType).all()
        assert len(existing_content_types) == 0
        id_content = add_content(user_a, hose, 'path', 'new-content-type')
        new_content_types = session.query(ContentType).all()
        assert len(new_content_types) == 1
        one_content_type = new_content_types[0]
        assert one_content_type.name == 'new-content-type'

    def test_create_content(self):
        id_user_a = create_hoseuser('user-a', 'test-a@test.com', 'hashedp')
        id_user_b = create_hoseuser('user-b', 'test-b@test.com', 'hashedpwd')
        session = Session()
        user_a = session.query(HoseUser).filter_by(name='user-a').one()
        user_b = session.query(HoseUser).filter_by(name='user-b').one()
        id_hose = create_hose(user_a, user_b)
        hose = session.query(Hose).filter_by(id_hose=id_hose).one()
        session.add(ContentType(id_content_type=0, name='content-type'))
        session.commit()
        id_content = add_content(user_a, hose, 'path', 'content-type')
        contents = session.query(Content).all()
        assert len(contents) == 1
        content = contents[0]
        assert content.id_user_origin == id_user_a
        assert content.id_hose == id_hose
        assert content.id_content_type == 0
