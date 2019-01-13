from django.contrib.auth.models import AbstractUser
from django.db import models


class HoseUser(AbstractUser):
    """
    Extended user class for a user of the app
    """
    def __str__(self):
        return self.email


class HoseAssociation(models.Model):
    """
    A HoseAssociation runs between two users
    and allows to share content through it
    """
    # first_end = models.OneToOneField(
    #     HoseUser,
    #     on_delete=models.CASCADE,
    #     primary_key=False,
    # )
    # second_end = models.OneToOneField(
    #     HoseUser,
    #     on_delete=models.CASCADE,
    #     primary_key=False,
    # )
    hose_name = models.CharField(max_length=200)
    time_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"'{self.hose_name}' created the {self.time_created}"


class HoseContent(models.Model):
    """
    Content shared by one user in a HoseAssociation
    """
    hose_from = models.ForeignKey(
        HoseAssociation,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=300, default='')
    times_listened = models.IntegerField(default=0)

    def __str__(self):
        return f"'{self.name}' linked to '{self.hose_from.hose_name}': {self.times_listened} times"