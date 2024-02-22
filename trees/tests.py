import random
from typing import Any, cast

from django.test import TestCase
from faker import Faker

from .factories import AccountFactory, TreeFactory, UserFactory
from .models import Account, PlantedTree, Tree, User

fake = Faker()


# Create your tests here.
class TestScenario(TestCase):

    def setUp(self):
        # Create two accounts
        self.account_1 = AccountFactory()
        self.account_2 = AccountFactory()

        # Create three users
        self.user_1 = UserFactory(account=self.account_1)
        self.user_2 = UserFactory(account=self.account_2)
        self.user_3 = UserFactory(account=[self.account_1, self.account_2])

        self.trees = [TreeFactory() for _ in range(10)]

        self.account_1 = cast(Account, self.account_1)
        self.account_2 = cast(Account, self.account_2)
        self.user_1 = cast(User, self.user_1)
        self.user_2 = cast(User, self.user_2)
        self.user_3 = cast(User, self.user_3)
        self.trees = cast(list[Tree], self.trees)

        self.user_1.plant_trees(
            [
                (random.choice(self.trees), (fake.latitude(), fake.longitude()))
                for _ in range(random.randint(5, 10))
            ],
            account=random.choice(self.user_1.accounts.all()),
        )
        self.user_2.plant_trees(
            [
                (random.choice(self.trees), (fake.latitude(), fake.longitude()))
                for _ in range(random.randint(5, 10))
            ],
            account=random.choice(self.user_2.accounts.all()),
        )
        self.user_3.plant_trees(
            [
                (random.choice(self.trees), (fake.latitude(), fake.longitude()))
                for _ in range(random.randint(5, 10))
            ],
            account=random.choice(self.user_3.accounts.all()),
        )

    def user_planted_trees(self):
        self.user_1 = cast(User, self.user_1)
        self.client.login(
            username=self.user_1.user.username, password="defaultpassword"
        )
        response = self.client.get("/")

        self.assertTemplateUsed(response, "trees/home.html")
        self.assertCountEqual(
            response.context["trees"],
            PlantedTree.objects.filter(planted_by=self.user_1),
        )

    def forbidden_user_planted_trees(self):
        self.user_1 = cast(User, self.user_1)
        self.user_2 = cast(User, self.user_2)
        self.client.login(
            username=self.user_1.user.username, password="defaultpassword"
        )
        response = self.client.get(
            f"/user/{PlantedTree.objects.filter(planted_by=self.user_2.pk)[0].pk}/"
        )

        self.assertEqual(response.status_code, 403)

    def account_planted_trees(self):
        self.user_1 = cast(User, self.user_1)
        self.client.login(
            username=self.user_1.user.username, password="defaultpassword"
        )

        account: Any = self.user_1.accounts.first()
        response = self.client.get(f"/account/{account.pk}/")

        self.assertTemplateUsed(response, "trees/account_trees.html")
        self.assertCountEqual(
            response.context["trees"], PlantedTree.objects.filter(account=account)
        )

    def test_plant_tree_1(self):
        self.user_1 = cast(User, self.user_1)
        self.trees = cast(list[Tree], self.trees)
        PlantedTree.objects.all().delete()
        self.user_1.plant_tree(
            tree=random.choice(self.trees),
            location=(fake.latitude(), fake.longitude()),
            account=random.choice(self.user_1.accounts.all()),
        )
        self.assertEqual(PlantedTree.objects.count(), 1)
        self.assertEqual(PlantedTree.objects.filter(planted_by=self.user_1).count(), 1)

    def test_plant_tree_2(self):
        self.user_2 = cast(User, self.user_2)
        self.trees = cast(list[Tree], self.trees)
        with self.assertRaises(ValueError):
            PlantedTree.objects.all().delete()
            self.user_2.plant_tree(
                tree=random.choice(self.trees),
                location=(fake.latitude(), fake.longitude()),
                account=self.account_2,
            )
        self.assertEqual(PlantedTree.objects.count(), 0)

    def test_plant_trees_1(self):
        self.user_1 = cast(User, self.user_1)
        self.trees = cast(list[Tree], self.trees)
        random_amount = random.randint(5, 10)
        PlantedTree.objects.all().delete()
        self.user_1.plant_trees(
            [
                (random.choice(self.trees), (fake.latitude(), fake.longitude()))
                for _ in range(random_amount)
            ],
            account=random.choice(self.user_1.accounts.all()),
        )
        self.assertEqual(PlantedTree.objects.count(), random_amount)
        self.assertEqual(
            PlantedTree.objects.filter(planted_by=self.user_1).count(), random_amount
        )

    def test_plant_trees_2(self):
        self.user_2 = cast(User, self.user_2)
        self.trees = cast(list[Tree], self.trees)
        with self.assertRaises(ValueError):
            PlantedTree.objects.all().delete()
            self.user_2.plant_trees(
                [
                    (random.choice(self.trees), (fake.latitude(), fake.longitude()))
                    for _ in range(random.randint(5, 10))
                ],
                account=self.account_2,
            )
        self.assertEqual(PlantedTree.objects.count(), 0)
