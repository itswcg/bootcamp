from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.follower} follow {self.followed}'

    @staticmethod
    def follow(from_user, to_user):
        Follow(follower=from_user,
               followed=to_user).save()

    @staticmethod
    def unfollow(from_user, to_user):
        f = Follow.objects.filter(follower=from_user, followed=to_user).all()
        if f:
            f.delete()

    @staticmethod
    def user_followed(from_user):
        followeders = Follow.objects.filter(follower=from_user).all()
        user_followed = []
        for followeder in followeders:
            user_followed.append(followeder.followed)
        return user_followed


