# Generated by Django 2.1.7 on 2019-03-19 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('room', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ExamGiven',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chat.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('surname', models.CharField(max_length=255, verbose_name='surname')),
                ('matriculation_number', models.IntegerField(unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chat.Course')),
            ],
        ),
        migrations.CreateModel(
            name='TaxRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chat.Student')),
            ],
        ),
        migrations.AddField(
            model_name='examgiven',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chat.Student'),
        ),
        migrations.AddField(
            model_name='exam',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chat.Professor'),
        ),
    ]
