# Generated by Django 3.0.8 on 2020-09-04 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='progressupdate',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='pledge',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pledges', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='pledge',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pledgetype', to='projects.Pledgetype'),
        ),
        migrations.AddField(
            model_name='pledge',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pledges', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_activity', to='projects.Location'),
        ),
        migrations.AddField(
            model_name='activity',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_activity', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_activity', to=settings.AUTH_USER_MODEL),
        ),
    ]
