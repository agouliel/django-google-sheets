from django.shortcuts import render, redirect
from .services import *
#from django.http import HttpResponseRedirect
from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            insert_row('db', form.cleaned_data['your_name'], form.cleaned_data['descr'], form.cleaned_data['pic_url'])
            # redirect to a new URL:
            #return HttpResponseRedirect("/thanks/")
            return redirect('photo-wall')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "name.html", {"form": form})

def photo_wall(request):
  photos = get_all_rows('db') # use the correct filename here
  return render(request, 'photo_wall.html', {'photos': photos})
