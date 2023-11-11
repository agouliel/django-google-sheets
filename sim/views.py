from django.shortcuts import render, redirect
from .services import *
#from django.http import HttpResponseRedirect
from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        
        # request.POST:
        # <QueryDict: {
        # 'csrfmiddlewaretoken': ['fuy2AFQD1N3LufZjs5ZeGrXTPDGiBUIYh7L4YmC2npPEhWSLtLKrTkciUvBtIUyx'],
        # 'your_name': ['Alexander'],
        # 'descr': ['The great'],
        # 'pic_url': ['https://upload.wikimedia.org/wikipedia/commons/8/84/Alexander_the_Great_mosaic_%28cropped%29.jpg']
        # }>
        # instead of the form, we could use:
        # name = request.POST.get('your_name', '')

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

    return render(request, 'name.html', {'form': form})

def photo_wall(request):
  photos = get_all_rows('db') # use the correct filename here
  # https://stackoverflow.com/questions/72899/how-to-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary-in-python
  reversedlist = sorted(photos, key=lambda d: d['id'], reverse=True)
  return render(request, 'photo_wall.html', {'photos': reversedlist})
