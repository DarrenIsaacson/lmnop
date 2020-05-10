from django.shortcuts import render, redirect, get_object_or_404


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


    usernotes = Note.objects.filter(user=user.pk).order_by('-posted_date')
    return render(request, 'lmn/users/user_profile.html', { 'user': user , 'notes': usernotes, })#'loggedIn': loggedIn


# View to power user editing their own profile
# shows form 
@login_required
def my_user_profile(request, user_pk):
    
    #add try/catch
    uProfile = get_object_or_404(UProfile, pk=user_pk)
    
    if UProfile.objects.filter(pk = user_pk).exists(): #https://stackoverflow.com/questions/11714536/check-if-an-object-exists
        if request.method == 'POST': 
            form = UserProfileForm(request.POST)
            if form.is_valid():
                uProfile = form.save(commit=False)
                uProfile.user_id = UProfile.objects.get(user_id=user_pk) #dont use request
                uProfile.save()
                #uProfile = UProfile.objects.get(pk=user_pk)
                return redirect('lmn:user_profile', uProfile.user_id) 
            else :
                message = 'Please check the data you entered'
                # probably redirect to this page again as a get requet? 
                return render(request, 'registration/edit-profile.html', {'form': form})
        else :
            #uProfile = UProfile.objects.get(pk=user_pk)
            form = UserProfileForm() ## figure out user profile object 
            return render(request, 'registration/edit-profile.html', {'form': form, 'user_pk':uProfile.pk }) # 
    else: # create a UProfile for user
        user = User.objects.get(pk=user_pk)
        UProfile.objects.create(user=user, birthday='', city='', state='', favoriteVenue='', favoriteArtist='', photo='', description='')

def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            UProfile.objects.create(user=user, birthday='', city='', state='', favoriteVenue='', favoriteArtist='', photo='', description='') 
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
