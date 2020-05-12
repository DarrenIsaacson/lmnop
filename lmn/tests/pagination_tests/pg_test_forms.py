from django.test import TestCase

from django.urls import reverse, resolve

from lmn.views_artists import artist_list
from lmn.views_notes import latest_notes
from lmn.views_users import user_profile
from lmn.views_venues import venue_list

