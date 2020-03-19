from django.shortcuts import render, redirect
from .forms import PersonForm
from .models import Person
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def home(request):  # TODO: add error presentation for user if errors pops up
    if request.method == 'POST':
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
            form_instance = Person.objects.create(household_no=household_no, last_name=last_name, first_name=first_name,
                                                  middle_name=middle_name, name_extension=name_extension, full_name=full_name, address=address,
                                                  birth_place=birth_place, birth_date=birth_date, gender=gender,
                                                  civil_status=civil_status, citizenship=citizenship,
                                                  occupation=occupation)
        else:
            messages.error(request, f'Person  is already in database. Please try again.')
            return redirect('forms-home')

    else:
        form = PersonForm
    return render(request, 'forms/home.html', {'form': form, 'title': 'Home'})


def about(request):
    return render(request, 'forms/about.html', {'title': 'About'})

