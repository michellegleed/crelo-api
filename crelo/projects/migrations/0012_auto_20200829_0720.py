# Generated by Django 3.0.8 on 2020-08-29 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_activity_object_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='object_id',
            field=models.IntegerField(),
        ),
    ]
