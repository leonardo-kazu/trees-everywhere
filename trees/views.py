from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView

from .forms import PlantTreeForm
from .models import Account, PlantedTree, User


class LoginView(View):
    def get(self, request: HttpRequest):
        return render(request, "trees/login.html")

    def post(self, request: HttpRequest):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request, "trees/login.html", {"error": "Invalid credentials."}
            )


@method_decorator(login_required, name="dispatch")
class LogoutView(View):

    def get(self, request: HttpRequest):
        logout(request)
        return redirect("login")


@method_decorator(login_required, name="dispatch")
class HomeView(View):
    def get(self, request: HttpRequest):
        user = User.objects.get(pk=request.user.pk)
        planted_trees = PlantedTree.objects.filter(planted_by=user)
        accounts = user.accounts.all()
        print(planted_trees[0].tree.name)
        return render(
            request, "trees/home.html", {"trees": planted_trees, "accounts": accounts}
        )


@method_decorator(login_required, name="dispatch")
class PlantedTreeDetailView(DetailView):
    model = PlantedTree
    template_name = "trees/planted_tree_detail.html"

    def get_queryset(self):
        # Only allow the user to view PlantedTree objects they are a part of
        queryset = super().get_queryset()
        return queryset.filter(planted_by=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj not in self.get_queryset():
            raise PermissionDenied("You are not allowed to view this PlantedTree")
        return obj


@method_decorator(login_required, name="dispatch")
class PlantTreeView(View):
    def get(self, request: HttpRequest):
        return render(request, "trees/plant_tree.html", {"form": PlantTreeForm()})

    def post(self, request: HttpRequest):
        form = PlantTreeForm(request.POST)
        if form.is_valid():
            tree = form.cleaned_data["tree"]
            latitude = form.cleaned_data["latitude"]
            longitude = form.cleaned_data["longitude"]
            account = form.cleaned_data["account"]
            try:
                User.objects.get(pk=request.user.pk).plant_tree(
                    tree, (latitude, longitude), account
                )
                redirect_url = (
                    reverse("home") + "?message=Tree%20planted%20successfully!"
                )
                return HttpResponseRedirect(redirect_url)
            except ValueError as e:
                return render(
                    request, "trees/plant_tree.html", {"form": form, "error": str(e)}
                )
        return render(request, "trees/plant_tree.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class AccountTreesView(View):
    def get(self, request: HttpRequest, account_id: int):
        user = User.objects.get(pk=request.user.pk)
        if not user.accounts.filter(pk=account_id).exists():
            raise PermissionDenied("You are not allowed to view this account")
        account = Account.objects.get(pk=account_id)
        trees = PlantedTree.objects.filter(account=account)
        return render(
            request,
            "trees/account_trees.html",
            {"trees": trees, "account": account.name},
        )
