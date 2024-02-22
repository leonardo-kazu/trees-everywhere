from django import forms

from .models import Account, Tree


class PlantTreeForm(forms.Form):
    """
    Plant tree form.

    One must pass the user as a keyword argument to the form.
    """

    def __init__(self, *args, **kwargs):
        self.user: str | None = kwargs.pop("user", None)
        super(PlantTreeForm, self).__init__(*args, **kwargs)
        self.fields["account"].queryset = Account.objects.filter(
            users=self.user, active=True
        )

    tree = forms.ModelChoiceField(queryset=Tree.objects.all())
    account = forms.ModelChoiceField(queryset=Account.objects.none())
    latitude = forms.DecimalField(max_digits=9, decimal_places=6)
    longitude = forms.DecimalField(max_digits=9, decimal_places=6)
