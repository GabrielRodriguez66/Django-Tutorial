import datetime
from django.db import models
from django.utils import timezone


class RecentQuestionManager(models.Manager):
    def published_recently(self):
        return [q for q in self.all().order_by('-pub_date')if q.was_published_recently()]


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    objects = RecentQuestionManager()

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    def has_choices(self):
        return self.choice_set.count() > 0


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
