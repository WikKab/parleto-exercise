from django import forms
from .models import Expense

DATE_CHOICES = (
    ('', ''),
    ('Ascending', 'Ascending'),
    ('Descending', 'Descending')
)


class ExpenseSearchForm(forms.ModelForm):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    first_category = forms.CharField(required=False, max_length=50)
    second_category = forms.CharField(required=False, max_length=50)
    sort_by_date = forms.ChoiceField(choices=DATE_CHOICES, initial='', required=False)

    class Meta:
        model = Expense
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
