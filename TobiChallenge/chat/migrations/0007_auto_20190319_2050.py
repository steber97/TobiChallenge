# Generated by Django 2.1.7 on 2019-03-19 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20190319_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='entities',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='score_top_intent',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='sentiment_analysis',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='top_scoring_intent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
