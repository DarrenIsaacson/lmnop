from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
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
    return render(request, 'lmn/users/user_profile.html', { 'user': user , 'notes': usernotes, })


# View to power user editing their own profile
# shows form 
@login_required
def my_user_profile(request, user_pk):
    
    uProfile = get_object_or_404(UProfile, pk=user_pk)
    if uProfile.user != request.user:
        return HttpResponseForbidden()

    if UProfile.objects.filter(pk = user_pk).exists(): #https://stackoverflow.com/questions/11714536/check-if-an-object-exists
        if request.method == 'POST': 
            form = UserProfileForm( request.POST, request.FILES, instance=request.user.uprofile)#Found request.Files in wishlist, instance solution at https://docs.djangoproject.com/
            if form.is_valid():
                uProfile = form.save(commit=False)
                uProfile.user_id = request.user.uprofile #connects the form with the related user to update the correct uprofile model object
                uProfile.save()                
                return redirect('lmn:user_profile', request.user.pk) 
            else :
                message = 'Please check the data you entered' 
                return render(request, 'registration/edit-profile.html', {'form': form})
        else :
            
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
