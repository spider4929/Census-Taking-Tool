from django.shortcuts import render, redirect
from .forms import PersonForm
from .models import Person
from .filters import PersonFilter
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def home(request):
    context = {
        'title': 'Home'
    }

    return render(request, 'forms/home.html', context)

@login_required
def create(request, id=0):  # TODO: add error presentation for user if errors pops up
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
                form.household_no = form.cleaned_data['household_no']
                form.last_name = form.cleaned_data['last_name'].upper()
                form.first_name = form.cleaned_data['first_name'].upper()
                form.middle_name = form.cleaned_data['middle_name'].upper()
                form.name_extension = form.cleaned_data['name_extension'].upper()
                form.full_name = f"{form.last_name}{form.name_extension}, {form.first_name} {form.middle_name}"
                form.address = form.cleaned_data['address'].upper()
                form.birth_place = form.cleaned_data['birth_place'].upper()
                form.birth_date = form.cleaned_data['birth_date']
                form.gender = form.cleaned_data['gender']
                form.civil_status = form.cleaned_data['civil_status']
                form.citizenship = form.cleaned_data['citizenship']
                form.occupation = form.cleaned_data['occupation'].upper()
                form.author = request.user
                form.save()

            else:
                messages.error(request, f'Person  is already in database. Please try again.')
                return redirect('forms-create')

        else:
            person = Person.objects.get(id=id)
            form = PersonForm(request.POST, instance=person)

            if form.is_valid():
                messages.success(request, f'Form updated successfully!')
                form.last_name = form.cleaned_data['last_name'].upper()
                form.first_name = form.cleaned_data['first_name'].upper()
                form.middle_name = form.cleaned_data['middle_name'].upper()
                form.name_extension = form.cleaned_data['name_extension'].upper()
                form.address = form.cleaned_data['address'].upper()
                form.birth_place = form.cleaned_data['birth_place'].upper()
                form.occupation = form.cleaned_data['occupation'].upper()
                form.full_name = f"{person.last_name}{person.name_extension}, {person.first_name} {person.middle_name}"
                form.author = request.user
                form.save()
                return redirect('forms-search')

            else:
                messages.error(request, f'No edits were made or the Person is already in database. Please try again.')
                return redirect('forms-create')



    context = {
        'title': 'Create',
        'form': form
    }

    return render(request, 'forms/create.html', context)


def about(request):
    context = {
        'title': 'About'
    }

    return render(request, 'forms/about.html', context)


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
def delete(request, id):
    person = Person.objects.get(id=id)
    person.delete()
    messages.success(request, f'Entry deleted successfully!')
    return redirect('forms-search')



