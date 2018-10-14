from typing import Union

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


def create_content(user_adding: HoseUser, hose: Hose, source_path: str, content_type: str) -> int:
    """
    A user can add content to the Hose

    :param user_adding:
    :param hose:
    :param source_path:
    :param content_type:
    :return:
    """
    session = Session()
    content_type = ContentType(name=content_type)
    session.add(content_type)
    content = Content(id_hose=hose.id_hose,
                      id_user_origin=user_adding.id_user,
                      id_content_type=content_type.id_content_type,
                      source_path=source_path)
    session.add(content)
    session.commit()
    id_content = content.id_content
    session.close()
    return id_content

