from django.contrib import admin
from.models import Person, Gender, NameExtension, CivilStatus, Citizenship, Household

admin.site.register(Person)
admin.site.register(Gender)
admin.site.register(NameExtension)
admin.site.register(CivilStatus)
admin.site.register(Citizenship)
admin.site.register(Household)
