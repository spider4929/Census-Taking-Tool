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
                household_no = form.cleaned_data['household_no']
                last_name = form.cleaned_data['last_name'].upper()
                first_name = form.cleaned_data['first_name'].upper()
                middle_name = form.cleaned_data['middle_name'].upper()
                name_extension = form.cleaned_data['name_extension'].upper()
                full_name = f"{last_name}{name_extension}, {first_name} {middle_name}"
                address = form.cleaned_data['address'].upper()
                birth_place = form.cleaned_data['birth_place'].upper()
                birth_date = form.cleaned_data['birth_date']
                gender = form.cleaned_data['gender']
                civil_status = form.cleaned_data['civil_status']
                citizenship = form.cleaned_data['citizenship']
                occupation = form.cleaned_data['occupation'].upper()
                form_instance = Person(household_no=household_no, last_name=last_name, first_name=first_name,
                                       middle_name=middle_name, name_extension=name_extension, full_name=full_name,
                                       address=address, birth_place=birth_place, birth_date=birth_date, gender=gender,
                                       civil_status=civil_status, citizenship=citizenship, occupation=occupation)
                form_instance.save()

            else:
                messages.error(request, f'Person  is already in database. Please try again.')
                return redirect('forms-create')

        else:
            person = Person.objects.get(id=id)
            form = PersonForm(request.POST, instance=person)

            if form.is_valid():
                messages.success(request, f'Form updated successfully!')
                last_name = form.cleaned_data['last_name'].upper()
                first_name = form.cleaned_data['first_name'].upper()
                middle_name = form.cleaned_data['middle_name'].upper()
                name_extension = form.cleaned_data['name_extension'].upper()
                person.full_name = f"{last_name}{name_extension}, {first_name} {middle_name}"
                form.save()

            else:
                messages.error(request, f'No edits were made or the Person  is already in database. Please try again.')
                return redirect('forms-create')

            context = {
                'title': 'Create',
                'form': form
            }

            return render(request, 'forms/edit.html', context)

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
    messages.success(request, f'Form deleted successfully!')
    return redirect('forms-search')



