from django.db import models
import bleach
from django.utils.html import escape
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _  # 延迟翻译
from bootcamp2.activities.models import Activity
import markdown


class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)
    parent = models.ForeignKey(
        'Feed', null=True, blank=True, on_delete=models.CASCADE)  # 数据库空值保存为NULL，允许输入一个空值
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def _str_(self):
        return self.post

    @staticmethod
    def get_feeds(from_feed=None):
        if from_feed is not None:
            feeds = Feed.objects.filter(
                parent=None, id__lte=from_feed)  # <= gte >=
        else:
            feeds = Feed.objects.filter(parent=None)
        return feeds

    @staticmethod
    def get_feeds_after(feed):
        feeds = Feed.objects.filter(parent=None, id__gt=feed)
        return feeds

    def get_comments(self):
        return Feed.objects.filter(parent=self).order_by('date')

    def comment(self, user, post):
        feed_comment = Feed(user=user, post=post, parent=self)
        feed_comment.save()
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return feed_comment

    def calculate_comments(self):
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return self.comments

    def get_content_as_markdown(self):
        return markdown.markdown(self.post, safe_mode='escape')

##
    def calculate_likes(self):
        likes = Activity.objects.filter(
            activity_type=Activity.LIKE, feed=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likes(self):
        likes = Activity.objects.filter(
            activity_type=Activity.LIKE, feed=self.pk)
        return likes

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers

    def linkfy_post(self):
        return bleach.linkify(escape(self.post))
