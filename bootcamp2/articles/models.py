from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
import markdown


# choice 最好在模型内部定义，然后给每个值定义一个合适名字的常量，方便外部引用
# on_delete 删除联级, related_name 不创建反向关联
class Article(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    content = models.TextField(max_length=4000)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(
        User, blank=True, null=True, related_name='+', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-create_date',)

    def __str__(self):
        return self.title

    def save(self, *args, **kw):
        if not self.pk:
            super(Article, self).save(*args, **kw)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = f'{self.pk}{self.title.lower()}'
            self.slug = slugify(slug_str)
        super(Article, self).save(*args, **kw)

    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')

    @staticmethod
    def get_published():
        articles = Article.objects.filter(status=Article.PUBLISHED)
        return articles

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(
                    tag=tag.lower(), article=self)

    def get_tags(self):
        return Tag.objects.filter(article=self)

    def get_summary(self):
        if len(self.content) > 255:
            return f'{self.content[:255]}...'
        else:
            return self.content

    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')

    def get_comments(self):
        return ArticleComment.objects.filter(article=self)

# 设置不重复的字段组合， 设置带有索引的字段组合


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('tag', 'article'),)
        index_together = [['tag', 'article'], ]

    def __str__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        count = {}
        for tag in Tag.objects.all():
            if tag.article.status != Article.PUBLISHED:
                continue
            if tag.tag in count:
                count[tag.tag] += 1
            else:
                count[tag.tag] = 1
        sorted_count = sorted(list(count.items()),
                              key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return f'{self.user.username} {self.article.title}'
