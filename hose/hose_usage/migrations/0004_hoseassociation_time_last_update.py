# Generated by Django 2.1.5 on 2019-01-13 22:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hose_usage', '0003_auto_20190113_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoseassociation',
            name='time_last_update',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
