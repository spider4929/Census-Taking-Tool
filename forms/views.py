from django.shortcuts import render, redirect
from .forms import PersonForm, HouseholdForm
from .models import Person, Household
from .filters import PersonFilter
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def home(request):
    user = request.user
    context = {
        'title': 'Home',
        'user': user
    }

    return render(request, 'forms/home.html', context)


@login_required
def create_person(request, id=0):  # TODO: add error presentation for user if errors pops up
    if request.method == 'GET':
        if id == 0:
            form = PersonForm()
        else:
            person = Person.objects.get(id=id)
            form = PersonForm(instance=person)

    else:
        if id == 0:
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
                    full_name = f"{last_name}{name_extension}, {first_name} {middle_name}"
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
            person = Person.objects.get(id=id)
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
                    person.full_name = f"{person.last_name}{person.name_extension}, {person.first_name} {person.middle_name}"
                person.author = request.user
                person.save()
                form.save()
                return redirect('forms-search')

            else:
                messages.error(request, f'No edits were made or the Person is already in database. Please try again.')
                return redirect('forms-create-person')

    context = {
        'title': 'Create Person',
        'form': form
    }

    return render(request, 'forms/create-person.html', context)


@login_required
def create_household(request, id=0):
    if request.method == 'GET':

        if id == 0:
            form = HouseholdForm

        else:
            household = Household.objects.get(id=id)
            form = PersonForm(instance=household)

    else:

        if id == 0:
            form = HouseholdForm(request.POST)

            if form.is_valid():
                messages.success(request, f'Form passed successfully!')
                form.save()

            else:
                messages.error(request, f'Household is already in database. Please try again.')
                return redirect('forms-create-household')

        else:
            household = Household.objects.get(id=id)
            form = HouseholdForm(request.POST, instance=household)
            if form.is_valid():
                messages.success(request, f'Entry edited successfully!')
                form.save()

            else:
                messages.error(request, f'No edits were made or the Household is already in database. Please try again.')
                return redirect('forms-create-household')

    context = {
        'title': 'Create Household',
        'form': form
    }

    return render(request, 'forms/create-household.html', context)


@login_required
def search(request):
    people = Person.objects.all()

    search_filter = PersonFilter(request.GET, queryset=people)
    people = search_filter.qs

    context = {
        'title': 'Search',
        'people': people,
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


@login_required
def delete(request, id):
    person = Person.objects.get(id=id)
    person.delete()
    messages.success(request, f'Entry deleted successfully!')
    return redirect('forms-search')


def about(request):
    context = {
        'title': 'About'
    }

    return render(request, 'forms/about.html', context)

