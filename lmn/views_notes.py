from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, NoteEditPhotoForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone


@login_required
def new_note(request, show_pk):
    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST':

        form = NewNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.posted_date = timezone.now()
            # note.photo = photo
            note.save()
            return redirect('lmn:note_detail', note_pk=note.pk)

    else:
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html', {'form': form, 'show': show})


def latest_notes(request):
    notes = Note.objects.all().order_by('posted_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(notes, 10)  # display maximum of 10 list of Notes per page
    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    return render(request, 'lmn/notes/note_list.html', {'notes': notes})


def notes_for_show(request, show_pk):  # pk = show pk

    notes = Note.objects.filter(show=show_pk).order_by('posted_date')
    show = Show.objects.get(pk=show_pk)
    return render(request, 'lmn/notes/note_list.html', {'show': show, 'notes': notes})


def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)

    if request.method == 'POST':
        photo_form = NoteEditPhotoForm(request.POST, request.FILES, instance=note)

        if photo_form.is_valid():
            photo_form.save()

        return redirect('lmn:note_detail', note_pk=note_pk)
    else:
        photo_form = NoteEditPhotoForm(instance=note)
    return render(request, 'lmn/notes/note_detail.html', {'note': note, 'photo_form': photo_form})
