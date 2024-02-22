from django.urls import path

from .views import APIPlantedTreesView

urlpatterns = [
    path(
        "me/planted_trees/", APIPlantedTreesView.as_view(), name="api_me_planted_trees"
    )
]
