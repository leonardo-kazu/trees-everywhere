from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from ..models import PlantedTree, User


@method_decorator(login_required, name="dispatch")
class APIPlantedTreesView(View):
    def get(self, request: HttpRequest):
        user = User.objects.get(pk=request.user.pk)
        planted_trees = PlantedTree.objects.filter(planted_by=user)
        return JsonResponse(
            {
                "planted_trees": [
                    {
                        "tree": {
                            "name": pt.tree.name,
                            "scientific_name": pt.tree.scientific_name,
                        },
                        "id": pt.pk,
                        "age": pt.age,
                        "planted_at": pt.planted_at,
                        "latitude": str(pt.latitude),
                        "longitude": str(pt.longitude),
                    }
                    for pt in planted_trees
                ]
            }
        )
