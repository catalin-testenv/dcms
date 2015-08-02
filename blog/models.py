

import datetime
from django.db import models
from django.utils import timezone
from django.core import validators
from django.core.exceptions import ValidationError

class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()

    def __unicode__(self):
        return '{self.first_name} {self.last_name}'.format(self=self)


class Label(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return '{self.name}'.format(self=self)


def validate_html(value):
    print('validate_html', value)
    if '<' in value:
        raise ValidationError(u'%s is not a valid value' % value)


class Article(models.Model):
    title = models.CharField(max_length=128, blank=False, validators=[validate_html])
    body = models.TextField()
    excerpt = models.TextField(max_length=256)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(Author)
    labels = models.ManyToManyField(Label)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __unicode__(self):
        return self.title


