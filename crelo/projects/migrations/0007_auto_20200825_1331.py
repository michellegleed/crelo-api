# Generated by Django 3.0.8 on 2020-08-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20200825_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='current_amount',
            field=models.IntegerField(default=0),
        ),
    ]
