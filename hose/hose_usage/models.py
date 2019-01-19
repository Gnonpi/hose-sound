from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class HoseUser(AbstractUser):
    """
    Extended user class for a user of the app
    """
    def __str__(self):
        return f"(username:{self.username}, email:{self.email})"


class HoseAssociation(models.Model):
    """
    A HoseAssociation runs between two users
    and allows to share content through it
    """
    first_end = models.ForeignKey(
        HoseUser,
        on_delete=models.CASCADE,
        related_name='first_end',
    )
    second_end = models.ForeignKey(
        HoseUser,
        on_delete=models.CASCADE,
        related_name='second_end',
    )
    hose_name = models.CharField(max_length=200)
    time_created = models.DateField(auto_now_add=True)
    time_last_update = models.DateTimeField(auto_now_add=True)

    def get_other_end(self, name):
        """
        Flip-flop ends of names

        :param name:
        :return:
        """
        if name == self.first_end.username:
            return self.second_end.username
        elif name == self.second_end.username:
            return self.first_end.username
        else:
            return ''
            # todo: add custom error
            # raise ValueError(f"Username '{name}' is not in Hose {self.hose_name}")

    def is_valid_association(self):
        """
        Check if association is a cycle

        :return:
        """
        if self.first_end.id == self.second_end.id:
            return False
        return True

    def as_dict(self):
        return {
            'hose_id': self.id,
            'first_end_id': self.first_end.id,
            'first_end_username': self.first_end.username,
            'second_end_id': self.second_end.id,
            'second_end_username': self.second_end.username,
            'hose_name': self.hose_name,
            'time_created': self.time_created,
            'time_last_update': self.time_last_update,
        }

    def __str__(self):
        return f"'{self.hose_name}'<{self.first_end}-{self.second_end}> created the {self.time_created}"


class HoseContent(models.Model):
    """
    Content shared by one user in a HoseAssociation
    """
    hose_from = models.ForeignKey(
        HoseAssociation,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=300, default='')
    time_added = models.DateTimeField(auto_now_add=True)
    times_listened = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.hose_from.time_last_update = datetime.now()

    def __str__(self):
        return f"'{self.name}'(added {self.time_added}) linked to '{self.hose_from.hose_name}': {self.times_listened} times"


class AssociationDemand(models.Model):
    """
    Demand of association between two users
    """
    MAX_DEMANDS_SENT = 3

    sender = models.ForeignKey(
        HoseUser,
        on_delete=models.CASCADE,
        related_name='sender'
    )
    receiver = models.ForeignKey(
        HoseUser,
        on_delete=models.CASCADE,
        related_name='receiver'
    )
    time_sent = models.DateTimeField(auto_now_add=True)
    caduce_at = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=15))

    def is_caduced(self):
        return timezone.now() > self.caduce_at

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.time_sent}"
