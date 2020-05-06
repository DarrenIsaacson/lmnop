from django.shortcuts import render, redirect

from .models import Venue, Artist, Note, Show
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
    return render(request, 'lmn/users/user_profile.html', { 'user': user , 'notes': usernotes })


# View to power user editing their own profile
# shows form 
@login_required
def my_user_profile(request, ):

    uProfile = UProfile.objects.get(pk=UProfile.user)
    user = User.objects.get(pk=user_pk)

    if uProfile.exsists():
        if request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                uProfile = form.save()
                return render(request, 'lmn:user_profile', uProfile=UProfile.user) ## todo fix syntax to reverse URL with user PK, this needs to be able to pass to 
            else :
                message = 'Please check the data you entered'
                # probably redirect to this page again as a get requet? 
                return render(request, 'lmn:user_profile')
        else :
            
            #form = UserProfileForm(uProfile) ## figure out user profile object 
            return render(request, 'registration/edit-profile.html', {'form': form}) # 
    else:
        uProfile = UProfile.objects.create(user=user)

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
