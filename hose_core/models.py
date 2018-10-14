import pendulum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from hose_core.config import POSTGRES_DSN

engine = create_engine(POSTGRES_DSN)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class HoseUser(Base):
    """
    Class representing a registered user who can use the app
    """
    __tablename__ = 'hoseuser'

    id_user = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String)

    date_joined = Column(DateTime, default=pendulum.now('UTC').to_datetime_string())

    # def __eq__(self, other):
    #     if not isinstance(other, HoseUser):
    #         return False
    #     return all([
    #         # self.id_user == other.id_user,
    #         self.name == other.name,
    #         self.email == other.email,
    #         self.hashed_password == other.hashed_password,
    #         self.date_joined == other.date_joined,
    #     ])

    def __repr__(self):
        return f"<HoseUser(id_user={self.id_user}, name={self.name}, email={self.email}, " \
               f"hashed_password={self.hashed_password}, date_joined={self.date_joined})>"

    def __str__(self):
        return f"HoseUser({self.id_user}) {self.name} of {self.email} since {self.date_joined}"


class Hose(Base):
    """
    Class that represent the link between two users, that they'll use to share music
    """
    __tablename__ = 'hose'

    id_hose = Column(Integer, primary_key=True)
    date_added = Column(DateTime, default=pendulum.now('UTC').to_datetime_string())

    id_user_a = Column(Integer, ForeignKey('hoseuser.id_user'), nullable=False)
    id_user_b = Column(Integer, ForeignKey('hoseuser.id_user'), nullable=False)

    contents = relationship(
        'Content',
        backref='content',
        cascade='delete',
        lazy='dynamic'
    )

    def __eq__(self, other):
        if not isinstance(other, Hose):
            return False
        return all([
            self.id_hose == other.id_hose,
            self.id_user_a == other.id_user_a,
            self.id_user_b == other.id_user_b,
            self.date_added == other.date_added,
            self.contents == other.contents,
        ])

    def __repr__(self):
        return f"<Hose(id_hose={self.id_hose}, id_user_a={self.id_user_a}, id_user_b={self.id_user_b}" \
               f", date_added={self.date_added})>"

    def __str__(self):
        return f"Hose between {self.id_user_a} and {self.id_user_b} created {self.date_added}"


class ContentType(Base):
    """
    Class that represent the type of added content (file, url, ...)
    """
    __tablename__ = 'content_type'

    id_content_type = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __eq__(self, other):
        if not isinstance(other, ContentType):
            return False
        return all([
            self.id_content_type == other.id_content_type,
            self.name == other.name,
        ])

    def __repr__(self):
        return f"<ContentType(id_content_type={self.id_content_type}, name={self.name})>"

    def __str__(self):
        return f"ContentType({self.id_content_type}): {self.name}"


class Content(Base):
    """
    Class that represent one element added to a hose to be accessed later
    """
    __tablename__ = 'content'

    id_content = Column(Integer, primary_key=True)
    id_hose = Column(Integer, ForeignKey('hose.id_hose'), nullable=False)
    id_user_origin = Column(Integer, ForeignKey('hoseuser.id_user'), nullable=False)
    id_content_type = Column(Integer, ForeignKey('content_type.id_content_type'), nullable=False)

    date_added = Column(DateTime, default=pendulum.now('UTC').to_datetime_string())
    source_path = Column(String, nullable=False)

    def __eq__(self, other):
        if not isinstance(other, Content):
            return False
        return all([
            self.id_content == other.id_content,
            self.id_hose == other.id_hose,
            self.id_user_origin == other.id_user_origin,
            self.id_content_type == other.id_content_type,
            self.date_added == other.date_added,
            self.source_path == other.source_path,
        ])

    def __repr__(self):
        return f"<Content(id_content={self.id_content}, id_hose={self.id_hose}, id_user_origin={self.id_user_origin}, " \
               f"id_content_type={self.id_content_type}, date_added={self.date_added}, source_path={self.source_path})>"

    def __str__(self):
        return f"Content({self.id_content}) added by user#{self.id_user_origin} in hose#{self.id_hose} " \
               f"on {self.date_added} linked to {self.source_path}"