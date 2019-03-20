# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(DegreeCourse)
admin.site.register(Professor)
admin.site.register(Exam)
admin.site.register(Student)
admin.site.register(ExamSubscription)
admin.site.register(ExamGiven)
admin.site.register(TaxRecord)
admin.site.register(Message)
admin.site.register(Chat)