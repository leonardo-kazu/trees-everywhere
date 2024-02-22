from django.contrib.auth.models import User as AuthUser
from django.db import models


# Create your models here.
class Account(models.Model):
    """
    Account model.

    This model represents an account in the system.

    Attributes:
    ===========
        name (str): The name of the account.
        created_at (datetime): The date and time the account was created.
        active (bool): A flag indicating whether the account is active.
    """

    name = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        """Return the name of the account."""
        return self.name


class Profile(models.Model):
    """
    Profile model.

    Represents the profile of an user.

    Attributes:
    ===========
        about (str): A brief description of the user.
        joined (datetime): The date and time the user joined the system.
    """

    about = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns the description (about) of the profile."""
        return self.about


class User(AuthUser):
    """
    User model.

    Represents an user of the system. Extends the base Django Auth User Model.

    Attributes:
    ===========
        profile (Profile): The profile of the user.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        """Return the username of the user."""
        return self.username


class AccountUser(models.Model):
    """
    AccountUser model.

    Represents the relationship between an account and an user.

    Attributes:
    ===========
        account (Account): The account.
        user (User): The user.
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return the name of the account and the username of the user."""
        return f"{self.account.name} - {self.user.username}"


class Tree(models.Model):
    """
    Tree model.

    Represents a tree in the system.

    Attributes:
    ===========
        name (str): The name of the tree.
        scientifc_name (str): The scientific name of the tree.
    """

    # TODO: Maybe add the total count of this tree in the system, instead of having to count it
    # TODO: every time from all the PlantedTree objects.
    name = models.CharField()
    scientific_name = models.CharField()

    def __str__(self):
        """Return the name of the tree."""
        return self.name


class PlantedTree(models.Model):
    """
    PlantedTree model.

    Represents a planted tree in the system.

    Attributes:
    ===========
        planted_by (User): The user who planted the tree.
        tree (Tree): The tree.
        age (int): The age of the tree in years.
        planted_at (datetime): The date and time the tree was planted.
        latitude (Decimal): The latitude of the location where the tree was planted.
        longitude (Decimal): The longitude of the location where the tree was planted.
    """

    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    planted_at = models.DateTimeField(auto_now_add=True)
    planted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        """Return the name of the tree and the username of the user who planted it."""
        return f"{self.tree.name} - {self.planted_by.username}"
