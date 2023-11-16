from django.shortcuts import render, redirect
from .services import *
#from django.http import HttpResponseRedirect
from .forms import *
import uuid
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.contrib.auth import get_user_model

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        
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
            if str(request.user) != 'AnonymousUser':
              insert_row('db', str(request.user), form.cleaned_data)
            # redirect to a new URL:
            #return HttpResponseRedirect("/thanks/")
            return redirect('photo-wall')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})

def photo_wall(request):
  if str(request.user) != 'AnonymousUser':
    photos = get_all_rows('db', str(request.user))
  else:
    photos = get_all_rows('db', 'welcome') # use the correct filename here
  # https://stackoverflow.com/questions/72899/how-to-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary-in-python
  reversedlist = sorted(photos, key=lambda d: d['id'], reverse=True)
  return render(request, 'photo_wall.html', {'photos': reversedlist})

def photo_view(request, photo_id):
  if str(request.user) != 'AnonymousUser':
    photo = get_one_row('db', str(request.user), int(photo_id))
  else:
    photo = get_one_row('db', 'welcome', 2)
  photo_dict = {'title': photo[0], 'description': photo[1], 'url': photo[2], 'id': photo[3]}
  return render(request, 'photo.html', {'photo': photo_dict})

def delete_view(request, photo_id):
    context = {}
 
    if request.method == 'POST':
        delete_row('db', str(request.user), int(photo_id))
        return redirect('photo-wall')
 
    return render(request, 'delete.html', context)

####################################################################
################### USING THE DATABASE #############################
####################################################################

def new_post_view(request):
  if request.method != 'POST':
    form = PostForm()
  else:
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      new_post = form.save(commit=False)
      new_post.user = request.user
      new_post.id = uuid.uuid4()
      # https://docs.djangoproject.com/en/dev/topics/i18n/timezones/
      # Django stores datetime information in UTC in the database
      new_post.post_date = timezone.now()
      new_post.save()
      post = Photos.objects.get(pk=new_post.id)
      compress_image(post.file.name)
      return redirect('home_db_url')
  return render(request, 'add_db.html', {'form': form})

def photo_wall_db_view(request):
  if str(request.user) != 'AnonymousUser':
    photos = Photos.objects.filter(user=request.user).order_by('-post_date')
  else:
    User = get_user_model()
    welcome_user = User.objects.get(username='welcome')
    photos = Photos.objects.filter(user=welcome_user)
  return render(request, 'photo_wall_db.html', {'photos': photos})

def post_db_view(request, post_id):
   post = Photos.objects.get(pk=post_id)
   return render(request, 'photo_db.html', {'photo': post})

class DeletePostView(DeleteView):
    template_name = 'delete.html'
    model = Photos
    success_url = reverse_lazy('home_db_url')