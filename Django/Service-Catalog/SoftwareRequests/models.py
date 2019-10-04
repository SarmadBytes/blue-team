from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Post1(models.Model):
    Answer_1 = models.CharField(max_length=500)
    Answer_2 = models.CharField(max_length=500)
    Answer_3 = models.CharField(max_length=500)
    Answer_4 = models.CharField(max_length=500)
    Answer_5 = models.CharField(max_length=500)
    Answer_6 = models.CharField(max_length=500)
    Answer_7 = models.CharField(max_length=500)
    Answer_8 = models.CharField(max_length=500)
    Answer_9 = models.CharField(max_length=500)
    Answer_10 = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
