# Generated by Django 2.2.5 on 2020-03-12 17:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('email_logger', '0002_emaillog_success'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaillog',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]