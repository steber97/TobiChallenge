# Generated by Django 2.1.7 on 2019-03-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_auto_20190320_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewIntent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1024)),
            ],
        ),
    ]
