from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User as BaseUser
from django.db import models


# Create your models here.
class Account(models.Model):
    """
    Account model.

    This model represents an account in the system.

    Attributes:
    ===========
        name (str): The name of the account.
        users (User): The users of the account.
        created_at (datetime): The date and time the account was created.
        active (bool): A flag indicating whether the account is active.
    """

    name = models.CharField()
    users = models.ManyToManyField("User", blank=True)
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


class User(models.Model):
    """
    User model.

    Represents an user of the system. Extends the base Django Auth User Model.

    Attributes:
    ===========
        user (BaseUser): The base user.
        accounts (Account): The accounts of the user.
        profile (Profile): The profile of the user.
    """

    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    accounts = models.ManyToManyField("Account", blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        """Return the username of the user."""
        return self.user.username

    def plant_tree(
        self, tree: Tree, location: tuple[Decimal, Decimal], account: Account.pk
    ):
        """
        Plant a tree.

        Args:
        =====
            tree (Tree): The tree to be planted.
            location (tuple[Decimal, Decimal]): The latitude and longitude of the location where the
            tree will be planted.
            account (Account.pk): The account where the tree will be planted.
        """
        planted_tree = PlantedTree(
            tree=tree,
            planted_by=self,
            account=account,
            latitude=location[0],
            longitude=location[1],
        )

        if account not in self.accounts.all():
            raise ValueError("The user is not part of the account")

        planted_tree.save()

    def plant_trees(
        self, plants: list[tuple[Tree, tuple[Decimal, Decimal]]], account: Account.pk
    ):
        """
        Plant multiple trees.

        Args:
        =====
            plants (list[tuple[Tree, tuple[Decimal, Decimal]]]): A list of tuples containing the
            tree and the location where it will be planted.
            account (Account.pk): The account where the trees will be planted.
        """
        for tree, location in plants:
            self.plant_tree(tree, location, account)


class PlantedTree(models.Model):
    """
    PlantedTree model.

    Represents a planted tree in the system.

    Attributes:
    ===========
        planted_by (User): The user who planted the tree.
        tree (Tree): The tree.
        planted_at (datetime): The date and time the tree was planted.
        latitude (Decimal): The latitude of the location where the tree was planted.
        longitude (Decimal): The longitude of the location where the tree was planted.
    """

    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    planted_at = models.DateTimeField(auto_now_add=True)
    planted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    @property
    def age(self):
        """Return the age of the tree in years."""
        return datetime.now().year - self.planted_at.year

    def __str__(self):
        """Return the name of the tree and the username of the user who planted it."""
        return f"{self.tree.name} - {self.planted_by.user.username}"
