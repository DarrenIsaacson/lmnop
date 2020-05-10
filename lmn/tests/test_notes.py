from django.test import TestCase, Client

from django.urls import reverse
from django.contrib import auth

from lmn.models import Venue, Artist, Note, Show
from django.contrib.auth.models import User 

import re, datetime
from datetime import timezone


class TestEmpyNotes(TestCase):
    
    def test_notes_page_with_no_notes(self):
        response = self.client.get(reverse('lmn:latest_notes'))
        self.assertFalse(response.context['notes'])
