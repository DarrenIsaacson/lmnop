from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

# Imported Paginator from Django Library
from django.core.paginator import Paginator


def venues_for_artist(request, artist_pk):   # pk = artist_pk

    """ Get all of the venues where this artist has played a show """

    shows = Show.objects.filter(artist=artist_pk).order_by('-show_date')  # most recent first
    artist = Artist.objects.get(pk=artist_pk)

    return render(request, 'lmn/venues/venue_list_for_artist.html', { 'artist' : artist, 'shows' :shows })


def artist_list(request):
    form = ArtistSearchForm()
    search_name = request.GET.get('search_name')
    if search_name:
        artists = Artist.objects.filter(name__icontains=search_name).order_by('name')
    else:
        artists = Artist.objects.all().order_by('name')

    paginator = Paginator(artists, 10) # Variable that takes in 2 arguments Paginator(Post items, how many items)

    # Variable that uses the http request.GET.get to gather the page number that will be passed to the view.
    page_number = request.GET.get('page')

    # Access the page by using the paginator method to get the corrisponding page. The notes variable will only contain 10 artist notes at a time
    artists = paginator.get_page(page_number)

    return render(request, 'lmn/artists/artist_list.html', { 'artists': artists, 'form': form, 'search_term': search_name })


def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk);
    return render(request, 'lmn/artists/artist_detail.html' , { 'artist': artist })
