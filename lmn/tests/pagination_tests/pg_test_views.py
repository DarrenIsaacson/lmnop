from django.test import TestCase, Client

from django.urls import reverse, resolve

from lmn.models import Venue, Artist, Note, Show

# from lmn.views_artists import artist_list
# from lmn.views_notes import latest_notes
# from lmn.views_users import user_profile
# from lmn.views_venues import venue_list

class PaginationExistTest(TestCase):
    fixtures = ['testing_artists', 'testing_venues', 'testing_shows']

    def test_artist_paginator(self):
        response = self.client.get(reverse('lmn:artist_list')
        self.assertEqual(2, response.count)


