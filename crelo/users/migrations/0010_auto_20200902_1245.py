# Generated by Django 3.0.8 on 2020-09-02 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20200901_2324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='favourite_categories',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='image',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='location',
        ),
    ]