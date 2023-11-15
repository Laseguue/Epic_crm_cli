# Generated by Django 4.2.7 on 2023-11-09 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='sales_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracts', to=settings.AUTH_USER_MODEL),
        ),
    ]
