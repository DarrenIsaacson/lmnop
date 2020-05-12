from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Imported Paginator from Django Library
from django.core.paginator import Paginator

def venue_list(request):
    form = VenueSearchForm()
    search_name = request.GET.get('search_name')

    if search_name:
        #search for this venue, display results
        venues = Venue.objects.filter(name__icontains=search_name).order_by('name')
    else :
        # created a paginator variable
        venues = Venue.objects.all().order_by('name')

    paginator = Paginator(venues, 10) # Variable that takes in 2 arguments Paginator(Post items, how many items)

    # Variable that uses the http request.GET.get to gather the page number that will be passed to the view.
    page_number = request.GET.get('page')

    # Access the page by using the paginator method to get the corrisponding page. The venues variable will only contain 10 Venue notes at a time
    venues = paginator.get_page(page_number)

    return render(request, 'lmn/venues/venue_list.html', { 'venues': venues, 'form': form, 'search_term': search_name })


def artists_at_venue(request, venue_pk):   # pk = venue_pk
    """ Get all of the artists who have played a show at the venue with pk provided """

    shows = Show.objects.filter(venue=venue_pk).order_by('-show_date') 
    venue = Venue.objects.get(pk=venue_pk)

    return render(request, 'lmn/artists/artist_list_for_venue.html', { 'venue': venue, 'shows': shows })


def venue_detail(request, venue_pk):
    venue = get_object_or_404(Venue, pk=venue_pk)
    return render(request, 'lmn/venues/venue_detail.html' , { 'venue': venue })
