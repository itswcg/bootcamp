from django.test import TestCase
from django.contrib.auth.models import User


class ProfileMethodTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='itswcg',
            email='i@itswcg.me',
            password='itswcg_password',
        )
        user.profile.url = 'https://itswcg.me/'
        user.save()

    def test_get_profile(self):
        user = User.objects.get(username='itswcg')

        url = user.profile.get_url()
        self.assertEqual(url, 'https://itswcg.me/')

        picture_url = user.profile.get_picture()
        self.assertEqual(picture_url, '/static/img/user.png')

        screen_name = user.profile.get_screen_name()
        self.assertEqual(screen_name, 'itswcg')
