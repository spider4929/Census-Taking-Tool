from re import A
from unicodedata import category
from django.shortcuts import render, redirect
from pandas import date_range
from .forms import PersonForm, HouseholdForm
from .models import Citizenship, Person, Household
from .filters import PersonFilter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from datetime import date, timedelta
import pandas
import operator

@login_required
def home(request):
    user = request.user
    context = {
        'title': 'Home',
        'user': user
    }

    return render(request, 'forms/home.html', context)


# CRUD FOR Person model
@login_required
def create_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)

        if form.is_valid():
            messages.success(request, f'Form passed successfully!')
            household_no = form.cleaned_data['household_no']
            last_name = form.cleaned_data['last_name'].upper()
            first_name = form.cleaned_data['first_name'].upper()
            middle_name = form.cleaned_data['middle_name'].upper()
            name_extension = form.cleaned_data['name_extension']
            if name_extension.name_extension == 'None':
                full_name = f"{last_name}, {first_name} {middle_name}"
            else:
                full_name = f"{last_name} {name_extension}, {first_name} {middle_name}"
            birth_place = form.cleaned_data['birth_place'].upper()
            birth_date = form.cleaned_data['birth_date']
            gender = form.cleaned_data['gender']
            civil_status = form.cleaned_data['civil_status']
            citizenship = form.cleaned_data['citizenship']
            occupation = form.cleaned_data['occupation'].upper()
            author = request.user
            instance = Person(household_no=household_no, full_name=full_name, last_name=last_name, first_name=first_name,
                              middle_name=middle_name, name_extension=name_extension, birth_place=birth_place,
                              birth_date=birth_date, gender=gender, civil_status=civil_status, citizenship=citizenship,
                              occupation=occupation, author=author)
            instance.save()

        else:
            messages.error(request, f'Person  is already in database. Please try again.')
            return redirect('forms-create-person')

    else:
        form = PersonForm()

    context = {
        'title': 'Create Person',
        'form': form
    }

    return render(request, 'forms/create-person.html', context)


@login_required
def edit_person(request, id):
    person = Person.objects.get(id=id)
    if person.author_id == request.user.id or request.user.is_superuser == 1:
        if request.method == 'POST':
            form = PersonForm(request.POST, instance=person)

            if form.is_valid():
                messages.success(request, f'Entry edited successfully!')
                person.last_name = form.cleaned_data['last_name'].upper()
                person.first_name = form.cleaned_data['first_name'].upper()
                person.middle_name = form.cleaned_data['middle_name'].upper()
                person.name_extension = form.cleaned_data['name_extension']
                person.birth_place = form.cleaned_data['birth_place'].upper()
                person.occupation = form.cleaned_data['occupation'].upper()
                if person.name_extension.name_extension == 'None':
                    person.full_name = f"{person.last_name}, {person.first_name} {person.middle_name}"
                else:
                    person.full_name = f"{person.last_name} {person.name_extension}, {person.first_name} {person.middle_name}"
                person.author = request.user
                person.save()
                form.save()
                return redirect('forms-search')

            else:
                messages.success(request, f'No edits were made or the Person is already in database. Please try again.')
                return redirect('forms-edit-person')

        else:  # GET request
            person = Person.objects.get(id=id)
            form = PersonForm(instance=person)

        context = {
            'title': 'Update Person',
            'form': form
        }

        return render(request, 'forms/edit-person.html', context)
    else:
        messages.success(request, f'You cannot edit an entry that you did not create.')
        return redirect('forms-search')


@login_required
def delete_person(request, id):
    person = Person.objects.get(id=id)
    if person.author_id == request.user.id or request.user.is_superuser == 1:
        person.delete()
        messages.success(request, f'Entry deleted successfully!')
        return redirect('forms-search')
    else:
        messages.success(request, f'You cannot delete an entry that you did not create.')
        return redirect('forms-search')


# CRUD FOR Household model
@login_required
def create_household(request):
    if request.method == 'POST':
        form = HouseholdForm(request.POST)

        if form.is_valid():
            messages.success(request, f'Form passed successfully!')
            household_no = form.cleaned_data['household_no']
            name = form.cleaned_data['name'].upper()
            address = form.cleaned_data['address'].upper()
            author = request.user
            instance = Household(household_no=household_no, name=name, address=address, author=author)
            instance.save()

        else:
            messages.success(request, f'Household is already in database. Please try again.')
            return redirect('forms-create-household')

    else:
        form = HouseholdForm()

    context = {
        'title': 'Create Household',
        'form': form
    }

    return render(request, 'forms/create-household.html', context)


@login_required
def edit_household(request, id):
    household = Household.objects.get(household_no=id)
    if household.author_id == request.user.id or request.user.is_superuser == 1:
        if request.method == 'POST':
            form = HouseholdForm(request.POST, instance=household)

            if form.is_valid():
                messages.success(request, f'Entry edited successfully!')
                household.household_no = form.cleaned_data['household_no']
                household.name = form.cleaned_data['name'].upper()
                household.address = form.cleaned_data['address'].upper()
                household.save()

            else:
                messages.success(request, f'No edits were made or the Household is already in database. Please try again.')
                return redirect('forms-create-household')

        else:
            household = Household.objects.get(household_no=id)
            form = HouseholdForm(instance=household)

        context = {
            'title': 'Update Household',
            'form': form
        }

        return render(request, 'forms/edit-household.html', context)
    else:
        messages.success(request, f'You cannot edit an entry that you did not create.')
        return redirect('forms-search')


@login_required
def delete_household(request, id):
    household = Household.objects.get(household_no=id)
    if household.author_id == request.user.id or request.user.is_superuser == 1:
        household.delete()
        messages.success(request, f'Entry deleted successfully!')
        return redirect('forms-search')
    else:
        messages.success(request, f'You cannot delete an entry that you did not create.')
        return redirect('forms-search')


@login_required
def search(request):
    people = Person.objects.all().order_by('household_no')
    households = Household.objects.all().order_by('household_no')

    search_filter = PersonFilter(request.GET, queryset=people)
    people = search_filter.qs

    context = {
        'title': 'Search',
        'people': people,
        'households': households,
        'search_filter': search_filter
    }

    return render(request, 'forms/search.html', context)


@login_required
def specify(request, id):
    person = Person.objects.get(id=id)

    context = {
        'title': 'Specify',
        'person': person
    }

    return render(request, 'forms/specify.html', context=context)


def about(request):
    context = {
        'title': 'About'
    }

    return render(request, 'forms/about.html', context)
 
def dashboard_with_pivot(request):
    return render(request, 'forms/dashboard_with_pivot.html', {})

def pivot_data(request):
    dataset = Person.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

def analytics_view(request):

    #for gender pie graph
    male_no = Person.objects.filter(gender='1').count()
    female_no = Person.objects.filter(gender='2').count()
    gender_list = ['Male', 'Female']
    gender_no = [male_no, female_no]

    #for civil status graph
    married_no = Person.objects.filter(civil_status='1').count()
    single_no = Person.objects.filter(civil_status='2').count()
    separated_no = Person.objects.filter(civil_status='3').count()
    widowed_no = Person.objects.filter(civil_status='4').count()
    civil_list = ['Married','Single','Separated','Widowed']
    civil_no = [married_no, single_no, separated_no, widowed_no ]
    
    #for citizenship graph
    filipino_no = Person.objects.filter(citizenship='1').count()
    foreigner_no = Person.objects.filter(citizenship='2').count()
    citizen_list = ['Filipino','Foreigner']
    citizen_no = [filipino_no, foreigner_no]

    #for age range graph
    startdate = date.today()

    age_0_10 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=3650),
        startdate
        ]).count()

    age_11_20 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=7300),
        startdate-timedelta(days=3649)
        ]).count()

    age_21_30 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=10950),
        startdate-timedelta(days=7299)
        ]).count()

    age_31_40 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=14600),
        startdate-timedelta(days=10949)
        ]).count()

    age_41_50 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=18250),
        startdate-timedelta(days=14599)
        ]).count()

    age_51_60 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=21900),
        startdate-timedelta(days=18249)
        ]).count()

    age_61_70 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=25550),
        startdate-timedelta(days=21899)
        ]).count()

    age_71_80 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=29200),
        startdate-timedelta(days=25549)
        ]).count()

    age_81_90 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=32850),
        startdate-timedelta(days=29199)
        ]).count()

    age_91_100 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=36500),
        startdate-timedelta(days=32849)
        ]).count()

    age_101_110 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=40150),
        startdate-timedelta(days=36499)
        ]).count()

    age_111_120 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=43800),
        startdate-timedelta(days=40149)
        ]).count()

    age_121_130 = Person.objects.filter(birth_date__range=[
        startdate-timedelta(days=47450),
        startdate-timedelta(days=43799)
        ]).count()

    age_list = [
        '0 to 10', 
        '11 to 20', 
        '21 to 30', 
        '31 to 40',
        '41 to 50',
        '51 to 60',
        '61 to 70',
        '71 to 80',
        '81 to 90',
        '91 to 100',
        '101 to 110',
        '111 to 120',
        '121 to 130'
    ]

    age_no = [
        age_0_10,
        age_11_20,
        age_21_30,
        age_31_40,
        age_41_50,
        age_51_60,
        age_61_70,
        age_71_80,
        age_81_90,
        age_91_100,
        age_101_110,
        age_111_120,
        age_121_130
    ]

    #for job distribution graph
    people = Person.objects.all()
    job_counter = {}

    for x in people:
        if x.occupation not in job_counter:
            job_counter[x.occupation] = 0
        job_counter[x.occupation] += 1

    sorted_job_counter = dict(sorted(job_counter.items(), key=operator.itemgetter(1),reverse=True))

    job_list = list(sorted_job_counter.keys())
    job_list = job_list[:10]
    job_no = list(sorted_job_counter.values())
    job_no = job_no[:10]

    #for street distribution
    family = Household.objects.all()
    street_counter = {
        "HARDBOARD ST.": 0,
        "B. PADILLA": 0,
        "E. MACLANG": 0,
        "BIENVENIDA": 0,
        "F. MANALO EXT.": 0,
        "L. GUNET": 0,
        "A. BONIFACIO": 0,
        "J. ANGELES": 0,
        "D. VICENCIO": 0,
        "L.H. REYES": 0,
        "M. MIRANDA": 0,
        "G. PLANA": 0,
        "V. CRUZ": 0,
        "E. SANTOS": 0,
        "N. AVERILLA": 0,
        "J. ASINAS": 0,
        "BARCELONA": 0,
        "H. CRUZ": 0,
        "P. PARADA": 0,
        "B.S. ANGELES": 0,
        "T. CLAUDIO": 0,
        "P. GUEVARRA": 0,
        "WILSON": 0
    }

    for x in family:
        for y in street_counter.keys():
            if y in x.address:
                street_counter[y] += 1
            else:
                pass

    sorted_street_counter = dict(sorted(street_counter.items(), key=operator.itemgetter(1),reverse=True))

    street_list = list(sorted_street_counter.keys())
    street_list = street_list[:10]
    street_no = list(sorted_street_counter.values())
    street_no = street_no[:10]




    context = {
        'gender_list': gender_list,
        'gender_no': gender_no,
        'civil_list': civil_list,
        'civil_no': civil_no,
        'citizen_list': citizen_list,
        'citizen_no': citizen_no,
        'age_list': age_list,
        'age_no': age_no,
        'job_list':job_list,
        'job_no':job_no,
        'street_list': street_list,
        'street_no': street_no
    }

    return render(request, 'forms/analytics.html', context)
    

