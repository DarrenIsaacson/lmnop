from django.test import TestCase, Client

from django.urls import reverse
from django.contrib import auth

from lmn.models import Venue, Artist, Note, Show
from django.contrib.auth.models import User 

import re, datetime
from datetime import timezone


class TestEmpyNotes(TestCase):

    # Test having no notes returns an empty list
    def test_notes_page_with_no_notes(self):
        response = self.client.get(reverse('lmn:latest_notes'))
        self.assertFalse(response.context['notes'])  # empty list is false

    def test_top_shows_page_with_no_notes(self):
        response = self.client.get(reverse('lmn:top_shows'))
        self.assertFalse(response.context['shows'])  # empty dictionary is false

    def test_notes_page_text_with_no_notes(self):
        response = self.client.get(reverse('lmn:latest_notes'))
        self.assertContains(response, 'No notes.')  # Check if "No notes." is on page text

    def test_top_shows_page_text_with_no_notes(self):
        response = self.client.get(reverse('lmn:top_shows'))
        self.assertContains(response, 'There are no notes yet check back later or add your own!')  # Check page text contains statement
    

class TestEditingNotes(TestCase):

    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

    def test_edit_note_saves(self):
        # Create new note
        new_note_url = reverse('lmn:new_note', kwargs={'show_pk':1})
        response = self.client.post(new_note_url, {'text':'This is test text.', 'title':'Test Title' }, follow=True)
        new_note = Note.objects.filter(text='This is test text.', title='Test Title').first()

        # Edit note
        edit_note_url = reverse('lmn:edit_note', kwargs={ 'note_pk': new_note.pk})
        edit_response = self.client.post(edit_note_url, { 'text': 'New text', 'title': 'New title'}, follow=True)

        # Assert redirected to note detail after edit
        self.assertRedirects(edit_response, reverse('lmn:note_detail', kwargs={ 'note_pk': new_note.pk}))
        
        # Test if original text not in note detail
        self.assertNotContains(edit_response, 'This is test text.')
        self.assertNotContains(edit_response, 'Test Title')

        # Test if new text in note detail
        self.assertContains(edit_response, 'New text')
        self.assertContains(edit_response, 'New title')
        

class TestDeletingNotes(TestCase):

    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)
    

    def test_delete_note(self):

        # Create test note
        new_note_url = reverse('lmn:new_note', kwargs={'show_pk':1})
        self.client.post(new_note_url, {'text':'This is test text.', 'title':'Test Title' }, follow=True)
        new_note = Note.objects.filter(text='This is test text.', title='Test Title').first()

        delete_note_url = reverse('lmn:delete_note', kwargs={ 'note_pk': new_note.pk })
        delete_response = self.client.post(delete_note_url, follow=True)

        # Assert redirected to latest notes
        self.assertRedirects(delete_response, reverse('lmn:latest_notes'))

        # Assert note is no longer in database
        deleted_note_query = Note.objects.filter(text='This is test text.', title='Test Title')
        self.assertEqual(deleted_note_query.count(), 0)


    def cancel_delete_note(self):

        # Create test note
        new_note_url = reverse('lmn:new_note', kwargs={'show_pk':1})
        self.client.post(new_note_url, {'text':'This is test text.', 'title':'Test Title' }, follow=True)
        new_note = Note.objects.filter(text='This is test text.', title='Test Title').first()

        delete_note_url = reverse('lmn:delete_note', kwargs={ 'note_pk': new_note.pk })
        delete_response = self.client.get(delete_note_url, follow=True)

        self.assertRedirects(delete_response, reverse('lmn:delete_note', kwargs={ 'note_pk': new_note.pk }))

        canceled_delete_query = Note.objects.filter(text='This is test text.', title='Test Title')
        self.assertEqual(canceled_delete_query.count(), 1)
        