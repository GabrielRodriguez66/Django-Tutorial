import datetime
from django.db import models
from django.utils import timezone


class RecentQuestionManager(models.Manager):
    def published_recently(self, last_n_questions):
        return self.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:last_n_questions]


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    objects = RecentQuestionManager()

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def has_choices(self):
        return self.choice_set.count() > 0


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
