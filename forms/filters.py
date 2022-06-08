import django_filters
from .models import *


class PersonFilter(django_filters.FilterSet):
    class Meta:
        model = Person
        fields = ['household_no', 'first_name']
