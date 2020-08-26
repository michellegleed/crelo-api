# Generated by Django 3.0.8 on 2020-08-26 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20200825_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='progressupdate',
            name='project_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
            preserve_default=False,
        ),
    ]