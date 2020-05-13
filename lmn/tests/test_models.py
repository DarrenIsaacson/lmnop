from django.test import TestCase

from django.contrib.auth.models import User, UProfile
from django.db import IntegrityError
# Create your tests here.


class TestUser(TestCase):

    def test_create_user_duplicate_username_fails(self):

        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_username_case_insensitive_fails(self):

        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='Bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_email_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_email_case_insensitive_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='another_bob', email='Bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()

<<<<<<< HEAD
<<<<<<< HEAD




=======
=======
>>>>>>> e7685314f524d9679c55296cdf0733139a8dfa00
#Test User Profile, create, update, save picture, delete picture
class TestUserProfile(TestCase):
    
    def test_create_user_profile(self):
        user = User(username='littleFoot', email='lilfoo@b4time.com', first_name='Little', last_name='Foot')
        user.save()

        uProfile = UProfile(user=0, birthday='', city='Minneapolis', state='MN', favoriteVenue='First Ave.', favoriteArtist='Kind Country', description='I love local music. Everything from Eydea & Abilities to Trampled by Turtles')
        uProfile.save()
        #check to make sure UProfile was created

    def test_update_user_profile(self):
        user = User(username='littleFoot', email='lilfoo@b4time.com', first_name='Little', last_name='Foot')
        user.save()

        uProfile = UProfile(user=0, birthday='', city='Minneapolis', state='MN', favoriteVenue='First Ave.', favoriteArtist='Kind Country', description='I love local music. Everything from Eydea & Abilities to Trampled by Turtles')
        uProfile.save()
        #check that user profile was updated


    def test_save_user_profile_picture(self):
        user = User(username='littleFoot', email='lilfoo@b4time.com', first_name='Little', last_name='Foot')
        user.save()

        uProfile = UProfile(user=0, birthday='', city='Minneapolis', state='MN', favoriteVenue='First Ave.', favoriteArtist='Kind Country', description='I love local music. Everything from Eydea & Abilities to Trampled by Turtles')
        uProfile.save()

        #add/save image and check that it is saved

    def test_delete_user_profile_picture(self):
        user = User(username='littleFoot', email='lilfoo@b4time.com', first_name='Little', last_name='Foot')
        user.save()
        #add image to profile creation
        uProfile = UProfile(user=0, birthday='', city='Minneapolis', state='MN', favoriteVenue='First Ave.', favoriteArtist='Kind Country', description='I love local music. Everything from Eydea & Abilities to Trampled by Turtles')
        uProfile.save()
        #test to make sure profile image is there
        #delete procifile picture and chech that it was deleted

    def test_change_user_profile_picture(self):
        user = User(username='littleFoot', email='lilfoo@b4time.com', first_name='Little', last_name='Foot')
        user.save()
        #add image to profile creation
        uProfile = UProfile(user=0, birthday='', city='Minneapolis', state='MN', favoriteVenue='First Ave.', favoriteArtist='Kind Country', description='I love local music. Everything from Eydea & Abilities to Trampled by Turtles')
        uProfile.save()
        #test to make sure profile image changed
<<<<<<< HEAD
        
>>>>>>> 44515f4... Refined database, created base test functions
=======
        
>>>>>>> e7685314f524d9679c55296cdf0733139a8dfa00
