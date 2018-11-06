import bcrypt
from sqlalchemy import Column, Binary

from hose_core.models import HoseUser


class LogHoseUser(HoseUser):
    hashed_password = Column(Binary(256))

    def __init__(self, password=None, **kwargs):
        super().__init__(**kwargs)
        if password is not None:
            self.set_password(password)
        else:
            self.hashed_password = None

    def set_password(self, password):
        """Set password."""
        self.hashed_password = bcrypt.hashpw(password, salt=bcrypt.gensalt(12))

    def check_password(self, value):
        """Check password."""
        return bcrypt.checkpw(self.hashed_password, value)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id_user

    def __repr__(self):
        return f"<HoseUser(id_user={self.id_user}, name={self.name}, email={self.email}, " \
               f"hashed_password={self.hashed_password}, date_joined={self.date_joined})>"
