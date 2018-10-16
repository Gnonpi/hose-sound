from typing import Union, List

from hose_core.exceptions import UserNotBelongingToHoseError, NoHoseBetweenUsersError
from hose_core.models import HoseUser, Session, Hose, Content, ContentType


def create_hoseuser(name: str, email: str, hashed_password: str) -> Union[int, None]:
    """
    Create a HoseUser

    :param name:
    :param email:
    :param hashed_password:
    :return:
    """
    session = Session()
    existing_user = session.query(HoseUser).filter_by(name=name).first()
    if existing_user is not None:
        return None
    user = HoseUser(name=name, email=email, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    id_user = user.id_user
    session.close()
    return id_user


def create_hose(user_a: HoseUser, user_b: HoseUser) -> Union[int, None]:
    """
    Create a Hose between users

    :param user_a:
    :param user_b:
    :return:
    """
    if user_a.id_user > user_b.id_user:
        user_a, user_b = user_b, user_a
    hose = Hose(id_user_a=user_a.id_user, id_user_b=user_b.id_user)
    session = Session()
    session.add(hose)
    session.commit()
    id_hose = hose.id_hose
    session.close()
    return id_hose


def get_hose_between_user(user_a: HoseUser, user_b: HoseUser) -> Union[int, None]:
    """
    Retrieve the Hose between two users, return None if there is no Hose

    :param user_a:
    :param user_b:
    :return:
    """
    if user_a.id_user > user_b.id_user:
        user_a, user_b = user_b, user_a
    session = Session()
    hose = session.query(Hose).filter_by(id_user_a=user_a.id_user, id_user_b=user_b.id_user).first()
    if hose is not None:
        return hose.id_hose
    else:
        return None


def add_content(user_adding: HoseUser, hose: Hose, source_path: str, content_type: str) -> int:
    """
    A user can add content to the Hose

    :param user_adding:
    :param hose:
    :param source_path:
    :param content_type:
    :return:
    """
    session = Session()
    if user_adding.id_user != hose.id_user_a and user_adding.id_user != hose.id_user_b:
        raise UserNotBelongingToHoseError(user_adding, hose)
    r_content_type = session.query(ContentType).filter_by(name=content_type).first()
    if r_content_type is None:
        r_content_type = ContentType(name=content_type)
        session.add(r_content_type)
    session.commit()
    content = Content(
        id_hose=hose.id_hose,
        id_user_origin=user_adding.id_user,
        id_content_type=r_content_type.id_content_type,
        source_path=source_path
    )
    session.add(content)
    session.commit()
    id_content = content.id_content
    session.close()
    return id_content


def get_content_for_user(user: HoseUser, other_user: HoseUser) -> Union[List[Content]]:
    """
    Retrieve all content available from a hose

    :param user:
    :param other_user:
    :return:
    """
    if user == other_user:
        return []
    id_hose = get_hose_between_user(user, other_user)
    if id_hose is None:
        raise NoHoseBetweenUsersError(user.id_user, other_user.id_user)
    session = Session()
    contents = session.query(Content).filter_by(id_hose=id_hose).all()
    return contents
