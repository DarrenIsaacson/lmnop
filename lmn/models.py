
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import datetime

# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
# User._meta.get_field('email')._unique = True
# User._meta.get_field('username')._unique = True


# Require email, first name and last name
# User._meta.get_field('email')._blank = False
# User._meta.get_field('last_name')._blank = False
# User._meta.get_field('first_name')._blank = False

User.email._unique = True
User.username.unique = True

User.email.blank = False
User.first_name.blank = False
User.last_name.blank = False


''' A music artist '''


class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return "Artist: " + self.name


''' A venue, that hosts shows. '''


class Venue(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=2, blank=False)  # What about international?

    def __str__(self):
        return 'Venue name: {} in {}, {}'.format(self.name, self.city, self.state)


''' A show - one artist playing at one venue at a particular date. '''


class Show(models.Model):
    
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False)
    url = models.CharField(max_length=400, blank=False)
    time = models.CharField(max_length=40, blank=False)
    ages = models.CharField(max_length=50, blank=False)
    show_date = models.DateTimeField(blank=False)

    def __str__(self):
        return 'Show with artist {} at {} on {}, {}. Ages {}'.format(self.artist, self.venue, self.show_date.date(), self.time, self.ages)


''' One user's opinion of one show. '''


class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(blank=False, auto_now=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def save(self, *args, **kwargs):

        prev_note = Note.objects.filter(pk=self.pk).first()
        if prev_note and prev_note.photo:
            if prev_note.photo != self.photo:
                self.delete_photo(prev_note.photo)
        super().save(*args, **kwargs)

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    def publish(self):
        posted_date = datetime.datetime.today()
        self.save()

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'No Photo Uploaded!'
        return 'Note for user ID {} for show ID {} with title {} text {} posted on {}'.format(self.user, self.show,
                                                                                              self.title, self.text,
                                                                                              self.posted_date)
