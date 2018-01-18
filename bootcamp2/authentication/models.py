from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save  # 监听信号


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    picture_url = models.CharField(max_length=50, null=True, blank=True)

    def get_url(self):
        url = self.url
        if not self.url.startswith("http://") \
                and not self.url.startswith("https://") \
                and len(self.url) > 0:
            url = "http://" + str(self.url)
        return url

    def get_picture(self):
        if not self.picture_url:
            no_picture = '/static/img/user/png'
            return no_picture
        return self.picture_url

    def get_screen_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.username


def create_user_profile(sender, instance, created, **kw):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kw):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
