# Generated by Django 2.1.7 on 2019-03-19 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20190319_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degreecourse',
            name='courses',
            field=models.ManyToManyField(blank=True, to='chat.Course'),
        ),
    ]
