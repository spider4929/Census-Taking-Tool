# Generated by Django 3.0.4 on 2020-10-25 08:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0002_person_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='citizenship',
            field=models.CharField(choices=[('FILIPINO', 'FILIPINO'), ('FOREIGNER', 'FOREIGNER')], help_text='Choose citizenship.', max_length=9),
        ),
        migrations.AlterField(
            model_name='person',
            name='civil_status',
            field=models.CharField(choices=[('MARRIED', 'MARRIED'), ('SINGLE', 'SINGLE'), ('SEPARATED', 'SEPARATED'), ('WIDOWED', 'WIDOWED')], help_text='Choose civil status.', max_length=9),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(help_text='Enter first name here.', max_length=40, validators=[django.core.validators.RegexValidator('^[a-zA-Z Ññ]*$', message='Only letters are allowed.')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='full_name',
            field=models.CharField(max_length=80, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z Ññ]*$', message='Only letters are allowed.')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='household_no',
            field=models.CharField(help_text='Enter household number here.', max_length=2, validators=[django.core.validators.RegexValidator('^[0-99999]*$', message='Only numbers are allowed.')]),
        ),
    ]
