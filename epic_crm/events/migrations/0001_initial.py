# Generated by Django 4.2.7 on 2023-11-09 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_start_date', models.DateTimeField()),
                ('event_end_date', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('attendees', models.IntegerField()),
                ('notes', models.TextField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='contracts.contract')),
            ],
        ),
    ]
