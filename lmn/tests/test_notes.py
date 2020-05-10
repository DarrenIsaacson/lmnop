from django.test import TestCase, Client

from django.urls import reverse
from django.contrib import auth

from lmn.models import Venue, Artist, Note, Show
from django.contrib.auth.models import User, Note, Venue, Artist, 

import re, datetime
from datetime import timezone