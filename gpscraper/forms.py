from django import forms
from django.core.validators import RegexValidator


validators = {
    'alphanumeric': RegexValidator(
        r'^[a-zA-Z0-9]*$', 'Only alphanumeric characters are allowed.'),
}


class SearchForm(forms.Form):

    query = forms.CharField(
        validators=[validators['alphanumeric']]
    )
