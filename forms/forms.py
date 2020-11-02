from django import forms
from .models import Person, Household
from django.utils.translation import gettext_lazy as _
from crispy_forms.layout import Layout, Submit


class DateInput(forms.DateInput):
    input_type = 'date'


class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = {'household_no', 'address'}


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = {'household_no', 'last_name', 'first_name', 'middle_name', 'name_extension', 'birth_place', 'birth_date',
                  'gender', 'civil_status', 'citizenship', 'occupation'}
        widgets = {
            'birth_date': DateInput(),
        }
        labels = {
            'name_extension': _('Name Extension'),
            'household_no': _('Household Number'),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper
    #     self.helper.form_method = 'POST'
    #     self.helper.layout = Layout(
    #         'household_no',
    #         'last_name',
    #         'first_name',
    #         'middle_name',
    #         'name_extension',
    #         'address',
    #         'birth_place',
    #         'birth_date',
    #         'gender',
    #         'civil_status',
    #         'citizenship',
    #         'occupation',
    #         Submit('submit', 'Submit', css_class='btn-success')
    #     )