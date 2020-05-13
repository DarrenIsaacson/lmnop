from django.test import TestCase, Client

from django.urls import reverse
from django.contrib import auth

from lmn.models import Venue, Artist, Note, Show
from django.contrib.auth.models import User

import re, datetime
from datetime import timezone


class TestEmptyViews(TestCase):

    def test_no_venues_redirect_into_empty_list(self):
        response = self.client.get(reverse('lmn:venue_list'))
        self.assertFalse(response.context['venues'])


class TestVenues(TestCase):
    fixtures = ['testing_venues', 'testing_artists', 'testing_shows', 'testing_users']

    def test_search_venue_with_no_macth(self):
        response = self.client.get(reverse('lmn:venue_list'), {'search_name': 'Blah blah'})
        self.assertNotContains(response, 'First Avenue')
        self.assertNotContains(response, 'The Turf Club')
        self.assertNotContains(response, 'Target Center')
        self.assertEqual(len(response.context['venues']), 0)
        self.assertTemplateUsed(response, 'lmn/venues/venue_list.html')

    def test_mark_non_existent_venue_returns_404(self):
        response = self.client.get(reverse('lmn:venue_detail', kwargs={'venue_pk': 10}))
        self.assertEqual(response.status_code, 404)


class TestAddNewVenue(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    def setUp(self):
        user = User.objects.get(pk=1)

        self.client.force_login(user)

    def test_add_new_venue_to_venue_list(self):
        response = self.client.post(reverse('lmn:venue_list'), {'name': 'First Avenue'}, follow=True)
        self.assertTemplateUsed(response, 'lmn/venues/venue_list.html')
        response_ven = response.context['venues']

        target_center_response = response_ven[0]
        target_center_in_database = Venue.objects.get(name='First Avenue')
        self.assertEqual(target_center_response, target_center_in_database)


class TestDeleteVenue(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)


class TestVenueDetail(TestCase):
    fixtures = ['testing_users', 'testing_artists', 'testing_shows', 'testing_venues', 'testing_notes']

    def setUp(self):
        user = User.objects.get(pk=1)

        self.client.force_login(user)

    def test_venue_detail(self):
        response = self.client.get(reverse('lmn:venue_detail', kwargs={'venue_pk': 1}))
        self.assertContains(response, 'First Avenue')
        self.assertEqual(response.context['venue'].name, 'First Avenue')
        self.assertEqual(response.context['venue'].pk, 1)

        self.assertTemplateUsed(response, 'lmn/venues/venue_detail.html')
