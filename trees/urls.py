from django.urls import include, path

from .views import (
    AccountTreesView,
    HomeView,
    LoginView,
    LogoutView,
    PlantedTreeDetailView,
    PlantTreeView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", HomeView.as_view(), name="home"),
    path("planted_tree/<int:pk>/", PlantedTreeDetailView.as_view(), name="tree_detail"),
    path("plant_tree/", PlantTreeView.as_view(), name="plant_tree"),
    path("account/<int:account_id>/", AccountTreesView.as_view(), name="account_trees"),
    path("api/", include("trees.api.urls"), name="api"),
]
