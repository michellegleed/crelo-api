# Generated by Django 3.0.8 on 2020-10-18 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_activity_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='pledge_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='view_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
