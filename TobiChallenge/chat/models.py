from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=255)
    cfu = models.IntegerField(blank=True,null=True)


class DegreeCourse(models.Model):
    name = models.CharField(verbose_name='Course', max_length=255)
    courses = models.ManyToManyField(Course, blank=True)


class Professor(models.Model):
    name = models.CharField(max_length=255)


class Exam(models.Model):
    date = models.DateTimeField()
    room = models.CharField(max_length=255)
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, blank=True, null=True)


class Student(models.Model):
    name = models.CharField(verbose_name='name', max_length=255)
    surname = models.CharField(verbose_name='surname', max_length=255)
    matriculation_number = models.IntegerField(unique=True)
    course = models.ForeignKey(DegreeCourse, on_delete=models.PROTECT, blank=True, null=True)


class ExamSubscription(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, blank=True, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.PROTECT, blank=True, null=True)


class ExamGiven(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, blank=True, null=True)
    mark = models.IntegerField()


class TaxRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, blank=True, null=True)
    amount = models.FloatField()


class Message(models.Model):
    vodafone_id = models.IntegerField(blank=True, null=True)
    text = models.TextField(max_length=1024, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    timestamp = models.TimeField(auto_now_add=True)
    top_scoring_intent = models.CharField(max_length=255, blank=True, null=True)
    score_top_intent = models.FloatField(blank=True, null=True)
    sentiment_analysis = models.FloatField(blank=True, null=True)
    # It is a JSON, list of strings of entities
    entities = models.TextField(max_length=1024, blank=True, null=True)


class Chat(models.Model):
    messages = models.ManyToManyField(Message)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
