# Generated by Django 3.2.7 on 2021-10-04 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_alter_project_author_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee_user_id',
            field=models.ForeignKey(blank=True, default=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_user_id', to=settings.AUTH_USER_MODEL), on_delete=django.db.models.deletion.CASCADE, related_name='assignee_user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='author_user_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
