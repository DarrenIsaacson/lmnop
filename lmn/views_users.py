from django.shortcuts import render, redirect

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Imported Paginator from Django Library
from django.core.paginator import Paginator

def user_profile(request, user_pk):

    """ 
    Summary line. 
  
    Extended description of function. 
  
    Parameters: 
    user :
    usernotes list(objects): Access the page by using the paginator method to get the corrisponding page. The notes variable will only contain 10 artist notes at a time
    paginator: Variable that takes in 2 arguments for the paginator ex: Paginator(Post items, how many items)
    page_number: Variable that uses the http request.GET.get to gather the page number that will be passed to the view.
  
    Returns: Directs them to html documentation with passing parameters
  
    """
    user = User.objects.get(pk=user_pk)
    usernotes = Note.objects.filter(user=user.pk).order_by('-posted_date')

    paginator = Paginator(usernotes, 5)# Variable that takes in 2 arguments Paginator(Post items, how many items)

    # Variable that uses the http request.GET.get to gather the page number that will be passed to the view.
    page_number = request.GET.get('page')

    # Access the page by using the paginator method to get the corrisponding page. The notes variable will only contain 10 notes at a time
    usernotes = paginator.get_page(page_number)
    
    return render(request, 'lmn/users/user_profile.html', { 'user': user , 'notes': usernotes })


@login_required
def my_user_profile(request):
    # TODO - editable version for logged-in user to edit own profile
    return redirect('lmn:user_profile', user_pk=request.user.pk)


def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('lmn:homepage')

        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form': form , 'message': message } )

    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form': form } )

def logout_view(request):
    #checks if user just logged out https://stackoverflow.com/questions/11393929/django-message-when-logout
    request.session['just_logged_out'] = True
    logout(request)
    return redirect('lmn:homepage', request)
