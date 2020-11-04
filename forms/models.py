from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

GENDER = (
    ('1', 'Male'),
    ('2', 'Female'),
)
CIVIL_STATUS = (
    ('1', 'Married'),
    ('2', 'Single'),
    ('3', 'Separated'),
    ('4', 'Widowed'),
)
CITIZENSHIP = (
    ('FILIPINO', 'Filipino'),
    ('FOREIGNER', 'Foreigner'),
)
NAME_EXTENSION = (
    ('1', 'Jr.'),
    ('2', 'Sr.'),
    ('3', 'II'),
    ('4', 'III'),
)

characters = RegexValidator(r'^[a-zA-Z Ññ]*$', message='Only letters are allowed.')
fullname_characters = RegexValidator(r'^[a-zA-Z Ññ ,]*$', message='Only letters are allowed.')
digits = RegexValidator(r'^[0-99999]*$', message='Only numbers are allowed.')


class Gender(models.Model):
    gender = models.CharField(max_length=6)  # gender, male or female

    def __str__(self):
        return self.gender


class NameExtension(models.Model):
    name_extension = models.CharField(max_length=4)  # name extensions (Sr., Jr., III, IV, etc.)

    def __str__(self):
        return self.name_extension


class CivilStatus(models.Model):
    civil_status = models.CharField(max_length=9)  # married, single, separated, widowed

    def __str__(self):
        return self.civil_status


class Citizenship(models.Model):
    citizenship = models.CharField(max_length=9)  # Filipino or Foreigner

    def __str__(self):
        return self.citizenship


class Household(models.Model):
    household_no = models.SmallIntegerField(help_text='Enter household number here.', primary_key=True)
    name = models.CharField(max_length=50, help_text='Enter a name for the household.')
    address = models.CharField(max_length=100, help_text='Enter house no. and street no.')  # house no. and street name only
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.household_no}. {self.name} household'


class Person(models.Model):
    household_no = models.ForeignKey(Household, on_delete=models.CASCADE, help_text='Choose household where person belong to.', null=True)
    full_name = models.CharField(max_length=240, unique=True, validators=[fullname_characters])  # full name, formatted like so {{Surname} {Extension}, {First Name} {Middle Name}}
    last_name = models.CharField(max_length=128, help_text='Enter surname here.', validators=[characters])  # surname
    first_name = models.CharField(max_length=128, help_text='Enter first name here.', validators=[characters])  # first name
    middle_name = models.CharField(max_length=64, blank=True, help_text='Enter middle name here, if needed.', validators=[characters])  # middle name
    name_extension = models.ForeignKey(NameExtension, on_delete=models.PROTECT, blank=True, help_text='Choose name extension, if needed.', default=5)  # name extensions (Sr., Jr., III, IV, etc.)
    birth_place = models.CharField(max_length=20, help_text='Enter city of birth only.')  # birth place, typically a city
    birth_date = models.DateField()  # birth date
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, help_text='Choose gender.', null=True)  # gender, male or female
    civil_status = models.ForeignKey(CivilStatus, on_delete=models.PROTECT, help_text='Choose civil status.', null=True)  # married, single, divorced, widowed
    citizenship = models.ForeignKey(Citizenship, on_delete=models.PROTECT, help_text='Choose citizenship.', null=True)  # Filipino or Foreigner
    occupation = models.CharField(max_length=40, help_text='Enter occupation here.')  # job
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.full_name


