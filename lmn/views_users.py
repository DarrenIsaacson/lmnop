from django.shortcuts import render, redirect

from .models import Venue, Artist, Note, Show, UProfile
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Public profile. Anyone may view.  
# If this is the logged in user, display button to go to edit profile
# Otherwise - not editable 
def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    '''loggedIn = False

    if user.is_authenticated():
        loggedIn = True
    else:
        return render without logged in request'''


    usernotes = Note.objects.filter(user=user.pk).order_by('-posted_date')
    return render(request, 'lmn/users/user_profile.html', { 'user': user , 'notes': usernotes, })#'loggedIn': loggedIn


# View to power user editing their own profile
# shows form 
@login_required
def my_user_profile(request, user_pk):
    
    #user = User.objects.get(pk=user_pk)
    #UProfile should have been created on User create
    #get user id from secondary key
    #add try/catch
    uProfile = UProfile.objects.get(user=user_pk)
    
    if UProfile.objects.filter(user = user_pk).exists(): #https://stackoverflow.com/questions/11714536/check-if-an-object-exists
        if request.method == 'POST': 
            form = UserProfileForm(request.POST)
            if form.is_valid():
                uProfile = form.save()
                ## I couldn't find a source for this syntax but following the other forms of rendering this seems it should be correct 
                return render(request, 'lmn:user_profile', {'uProfile': uProfile,}) 
            else :
                message = 'Please check the data you entered'
                # probably redirect to this page again as a get requet? 
                return render(request, 'lmn:user_profile')
        else :
            
            form = UserProfileForm() ## figure out user profile object 
            return render(request, 'registration/edit-profile.html', {'form': form }) # 
    else: # create a UProfile for user
        UProfile.objects.create(user=user, birthday='', city='', state='', favoriteVenue='', favoriteArtist='', profilePicture='', description='')

def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            UProfile.objects.create(user=user, birthday='', city='', state='', favoriteVenue='', favoriteArtist='', profilePicture='', description='') 
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
