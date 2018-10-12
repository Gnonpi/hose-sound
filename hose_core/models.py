import pendulum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class HoseUser(Base):
    __tablename__ = 'hoseuser'

    id_user = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String)

    date_joined = Column(DateTime, default=pendulum.now('UTC').to_datetime_string())

    def __repr__(self):
        return f"<HoseUser(id_user={self.id_user}, name={self.name}, email={self.email}, " \
               f"hashed_password={self.hashed_password}, date_joined={self.date_joined})>"

    def __str__(self):
        return f"HoseUser({self.id_user}) {self.name} of {self.email} since {self.date_joined}"


class Hose(Base):
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

    def __repr__(self):
        return f"<Hose(id_hose={self.id_hose}, id_user_a={self.id_user_a}, id_user_b={self.id_user_b}" \
               f", date_added={self.date_added})>"

    def __str__(self):
        return f"Hose between {self.id_user_a} and {self.id_user_b} created {self.date_added}"


class ContentType(Base):
    __tablename__ = 'content_type'

    id_content_type = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<ContentType(id_content_type={self.id_content_type}, name={self.name})>"

    def __str__(self):
        return f"ContentType({self.id_content_type}): {self.name}"


class Content(Base):
    __tablename__ = 'content'

    id_content = Column(Integer, primary_key=True)
    id_hose = Column(Integer, ForeignKey('hose.id_hose'), nullable=False)
    id_user_origin = Column(Integer, ForeignKey('hoseuser.id_user'), nullable=False)

    id_content_type = Column(Integer, ForeignKey('content_type.id_content_type'), nullable=False)