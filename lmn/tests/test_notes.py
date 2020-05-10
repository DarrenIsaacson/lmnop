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
    
