from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _


class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(blank=True, null=True)
    question = models.IntegerField(blank=True, null=True)
    answer = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.activity_type


class Notification(models.Model):
    LIKED = 'L'
    COMMENTED = 'C'
    FAVORITED = 'F'
    ANSWERED = 'A'
    ACCEPTED_ANSWER = 'W'
    EDITED_ARTICLE = 'E'
    ALSO_COMMENTED = 'S'
    FOLLOW = 'O'

    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (FAVORITED, 'Favorited'),
        (ANSWERED, 'Answered'),
        (ACCEPTED_ANSWER, 'Accepted Answer'),
        (EDITED_ARTICLE, 'Edited Article'),
        (ALSO_COMMENTED, 'Also Commented'),
        (FOLLOW, 'Follow'),
    )

    _LIKED_TEMPLATE = (
        '<a href="/{0}/">{1}</a> %s <a href="/feeds/{2}/">{3}</a>'
    ) % _('liked your post:')
    _COMMENTED_TEMPLATE = (
        '<a href="/{0}/">{1}</a> %s <a href="/feeds/{2}/">{3}</a>'
    ) % _('commented on your post:')
    _FAVORITED_TEMPLATE = (
        '<a href="/{0}/">{1}</a> %s <a href="/questions/{2}/">{3}</a>'
    ) % _('favorited your question:')
    _ANSWERED_TEMPLATE = (
        '<a href="/{0}/">{1}</a> %s <a href="/questions/{2}/">{3}</a>'
    ) % _('answered your question:')
    _ACCEPTED_ANSWER_TEMPLATE = (
        '<a href="/{0}/">{1}</a> %s <a href="/questions/{2}/">{3}</a>'
    ) % _('accepted your answer: ')
    _EDITED_ARTICLE_TEMPLATE = (
        '<a href="/{0}/">{1}</a> %s <a href="/article/{2}/">{3}</a>'
    ) % _('edited your article:')
    _ALSO_COMMENTED_TEMPLATE = (
        '<a href="/{0}/">{1}</a> %s <a href="/feeds/{2}/">{3}</a>'
    ) % _('also commented on the post:')
    _FOLLOW_TEMPLATE = (
        '<a href="/{0}/">{1}</a> 关注了你'
    )

    from_user = models.ForeignKey(
        User, related_name='+', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='+', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey('feeds.Feed', blank=True, null=True,
                             on_delete=models.CASCADE)
    question = models.ForeignKey(
        'questions.Question', blank=True, null=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(
        'questions.Answer', blank=True, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(
        'articles.Article', blank=True, null=True, on_delete=models.CASCADE)
    notification_type = models.CharField(
        max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
            )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
            )
        elif self.notification_type == self.FAVORITED:
            return self._FAVORITED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.question.pk,
                escape(self.get_summary(self.question.title))
            )
        elif self.notification_type == self.ANSWERED:
            return self._ANSWERED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.question.pk,
                escape(self.get_summary(self.question.title))
            )
        elif self.notification_type == self.ACCEPTED_ANSWER:
            return self._ACCEPTED_ANSWER_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.answer.question.pk,
                escape(self.get_summary(self.answer.description))
            )
        elif self.notification_type == self.EDITED_ARTICLE:
            return self._EDITED_ARTICLE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.article.slug,
                escape(self.get_summary(self.article.title))
            )
        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
            )
        elif self.notification_type == self.FOLLOW:
            return self._FOLLOW_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
            )

        return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 10
        if len(value) > summary_size:
            return f'{value[:summary_size]}...'
        return value
