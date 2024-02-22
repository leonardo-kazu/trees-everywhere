from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Account, PlantedTree, Profile, Tree, User


class UserAdmin(admin.ModelAdmin):
    """Extends the user admin model to show a horizontal filter for the accounts."""

    filter_horizontal = ("accounts",)


class AccountAdmin(admin.ModelAdmin):
    """
    Extends the account admin model to show a horizontal filter for the users.
    While also adding some filters, more information to the list display and editable values.
    """

    filter_horizontal = ("users",)
    list_display = ("name", "created_at", "active")
    list_filter = ("active",)
    list_editable = ("active",)


class TreeAdmin(admin.ModelAdmin):
    """
    Extends the tree admin model to show a list of the planted trees that are part of the tree.
    It also makes it so it returns a link to the PlantedTree object in the admin.

    """

    readonly_fields = ("planted_trees_objects",)

    def planted_trees_objects(self, obj):
        # Get all PlantedTrees objects this tree is a part of
        planted_trees = PlantedTree.objects.filter(tree=obj)
        # Create an HTML list representation of these objects
        list_items = "".join(
            [
                format_html(
                    "<li>Account: <a href='{}'>{}</a> - User: <a href='{}'>{}</a></li>",
                    reverse("admin:trees_account_change", args=(pt.account.pk,)),
                    pt.account.name,
                    reverse("admin:trees_user_change", args=(pt.planted_by.pk,)),
                    pt.planted_by,
                )
                for pt in planted_trees
                # f'<li>{pt} - <a href="'
                # + f'{reverse("admin:trees_user_change", args=(pt.planted_by.pk,))}'
                # + f"</a>{pt.planted_by}</li>"
                # for pt in planted_trees
            ]
        )
        return mark_safe(f"<ul>{list_items}</ul>")

    planted_trees_objects.allow_tags = True
    planted_trees_objects.short_description = "Planted Trees"


class ProfileAdmin(admin.ModelAdmin):
    """Extends the profile admin model to make the joined field read-only."""

    readonly_fields = ("joined",)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Tree, TreeAdmin)
