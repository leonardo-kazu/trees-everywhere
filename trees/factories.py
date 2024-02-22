from django.contrib.auth.models import User as BaseUser
from factory import Faker, PostGeneration, PostGenerationMethodCall, SubFactory, django

from .models import Account, Profile, Tree, User


class AccountFactory(django.DjangoModelFactory):
    class Meta:
        model = Account

    name = Faker("company")


class ProfileFactory(django.DjangoModelFactory):
    class Meta:
        model = Profile

    about = Faker("text")


class BaseUserFactory(django.DjangoModelFactory):
    class Meta:
        model = BaseUser

    username = Faker("user_name")
    email = Faker("email")
    password = PostGenerationMethodCall("set_password", "defaultpassword")


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    user = SubFactory(BaseUserFactory)
    profile = SubFactory(ProfileFactory)

    @PostGeneration
    def accounts(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for account in extracted:
                self.accounts.add(account)  # type: ignore
        else:
            account = AccountFactory()
            self.accounts.add(account)  # type: ignore


class TreeFactory(django.DjangoModelFactory):
    class Meta:
        model = Tree

    name = Faker("word")
    scientific_name = Faker("word")
