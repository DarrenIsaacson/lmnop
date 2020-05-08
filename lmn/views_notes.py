from django.shortcuts import render, redirect, get_object_or_404

from .models import Venue, Artist, Note, Show
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, EditNoteForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



@login_required
def new_note(request, show_pk):

    show = get_object_or_404(Show, pk=show_pk)

    if request.method == 'POST' :

        form = NewNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.show = show
            note.save()
            return redirect('lmn:note_detail', note_pk=note.pk)

    else :
        form = NewNoteForm()

    return render(request, 'lmn/notes/new_note.html' , { 'form': form , 'show': show })


def latest_notes(request):
    notes = Note.objects.all().order_by('-posted_date')
    return render(request, 'lmn/notes/note_list.html', { 'notes': notes })


def notes_for_show(request, show_pk):   # pk = show pk

    # Notes for show, most recent first
    notes = Note.objects.filter(show=show_pk).order_by('-posted_date')
    show = Show.objects.get(pk=show_pk)  
    return render(request, 'lmn/notes/note_list.html', { 'show': show, 'notes': notes } )


def note_detail(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)
    return render(request, 'lmn/notes/note_detail.html' , { 'note': note })

# Added function to edit notes 
def edit_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)

    if request.method == 'POST' :

        form = EditNoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect('lmn:note_detail', note_pk=note.pk)  # After note is updated redirect to the note_detail page

    else:
        # New edit note form with current note details (Ex. Title, Text)
        form = EditNoteForm(instance=note)

    return render(request, 'lmn/notes/edit_note.html', { 'form': form, 'note': note })


def delete_note(request, note_pk):
    note = get_object_or_404(Note, pk=note_pk)

    if request.method == 'POST':
        note.delete()
        return redirect('lmn:latest_notes')
    context = {
        'note': note,
    }
    return render(request, 'lmn/notes/delete_note.html', context)


def top_shows(request):
    shows = list(Show.objects.all())
    show_dict = {}
    num_of_shows_dict = {}
    for show in shows:
        num_of_notes = Note.objects.filter(show_id=show.id).count()
        num_of_shows_dict[show] = num_of_notes
    
    num_of_shows_dict = sorted(num_of_shows_dict.items(), key=lambda item: item[1], reverse=True)
    for show in num_of_shows_dict:
        notes = list(Note.objects.filter(show_id=show[0].id))
        show_dict[show[0]] = notes

    return render(request, 'lmn/notes/top_shows.html', { 'shows': show_dict })
