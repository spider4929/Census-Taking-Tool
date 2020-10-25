from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.conf import settings

GENDER = (
    ('MALE', 'Male'),
    ('FEMALE', 'Male'),
)
CIVIL_STATUS = (
    ('MARRIED', 'Married'),
    ('SINGLE', 'Single'),
    ('SEPARATED', 'Separated'),
    ('WIDOWED', 'Widowed'),
)
CITIZENSHIP = (
    ('FILIPINO', 'Filipino'),
    ('FOREIGNER', 'Foreigner'),
)
NAME_EXTENSION = (
    (' JR.', 'Jr.'),
    (' SR.', 'Sr.'),
    (' II', 'II'),
    (' III', 'III'),
)

characters = RegexValidator(r'^[a-zA-Z Ññ]*$', message='Only letters are allowed.')
fullname_characters = RegexValidator(r'^[a-zA-Z Ññ]*$', message='Only letters are allowed.')
digits = RegexValidator(r'^[0-99999]*$', message='Only numbers are allowed.')


class Person(models.Model):
    household_no = models.SmallIntegerField(help_text='Enter household number here.')
    full_name = models.CharField(max_length=240, unique=True, validators=[fullname_characters])  # full name, formatted like so {{Surname} {Extension}, {First Name} {Middle Name}}
    last_name = models.CharField(max_length=128, help_text='Enter surname here.', validators=[characters])  # surname
    first_name = models.CharField(max_length=128, help_text='Enter first name here.', validators=[characters])  # first name
    middle_name = models.CharField(max_length=64, blank=True, help_text='Enter middle name here.', validators=[characters])  # middle name
    name_extension = models.CharField(max_length=4, blank=True, choices=NAME_EXTENSION, help_text='Choose name extension, if required.')  # name extensions (Sr., Jr., III, IV, etc.)
    address = models.CharField(max_length=100, help_text='Enter house no. and street no.')  # house no. and street name only
    birth_place = models.CharField(max_length=20, help_text='Enter city of birth only.')  # birth place, typically a city
    birth_date = models.DateField()  # birth date
    gender = models.CharField(max_length=6, choices=GENDER, help_text='Choose gender.')  # gender, male or female
    civil_status = models.CharField(max_length=9, choices=CIVIL_STATUS, help_text='Choose civil status.')  # married, single, divorced, widowed
    citizenship = models.CharField(max_length=9, choices=CITIZENSHIP, help_text='Choose citizenship.')  # Filipino or Foreigner
    occupation = models.CharField(max_length=40, help_text='Enter occupation here.')  # job
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.full_name


