# Generated by Django 4.2.7 on 2023-11-14 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0006_alter_contract_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]