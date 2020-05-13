from django.db import models
from django.db.models.signals import post_save #https://stackoverflow.com/questions/11488974/django-create-user-profile-on-user-creation
from django.contrib.auth.models import User
import datetime

# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.
User._meta.get_field('email')._unique = True

#Require email, first name and last name
User._meta.get_field('email')._blank = False
User._meta.get_field('last_name')._blank = False
User._meta.get_field('first_name')._blank = False


''' A music artist '''
class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False);

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
        return 'Show with artist {} at {}, featuring {}, link: {}, starting at {}, ages {}, on {} '.format(self.artist, self.venue, self.name, self.url, self.time, self.ages, self.show_date)


''' One user's opinion of one show. '''
class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(blank=False, auto_now=True)

    def publish(self):
        posted_date = datetime.datetime.today()
        self.save()

    def __str__(self):
        return 'Note for user ID {} for show ID {} with title {} text {} posted on {}'.format(self.user, self.show, self.title, self.text, self.posted_date)

#user profile table
class UProfile(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)
    birthday = models.CharField(max_length=8, blank=True, null=True) #blank is for form validation
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)#change this to true to allow null feilds
    favoriteVenue = models.CharField(max_length=200, blank=True, null=True)
    favoriteArtist = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    description = models.TextField(max_length=3000, blank=True, null=True)

    '''def save(self, *args, **kwargs):
        uProfile= UProfile.objects.filter(pk=self.pk).first()

        if uProfile and uProfile.photo:
            if uProfile.photo != self.photo:
                self.delete_photo(uProfile.photo)
        super().save(*args, **kwargs)

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)'''
    
    def __str_(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        return 'User ID = {}, Birthday = {}, City = {}, State = {}, Favorite Venue = {}, Favorite Artist = {}, Profile Picture {}, Description = {}'.format(self.user, self.fName, self.lName, self.birthday, self.city, self.state, self.favoriteVenue, self.favoriteArtist, self.photo_str, self.description)
