import django_filters
from .models import *

class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = ['ctc','stipend','Role_offered','Spoc','hiring_who']