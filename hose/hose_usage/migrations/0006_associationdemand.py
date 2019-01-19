# Generated by Django 2.1.5 on 2019-01-19 12:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hose_usage', '0005_hosecontent_time_added'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociationDemand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('caduce_at', models.DateTimeField(default=datetime.datetime(2019, 2, 3, 13, 49, 32, 252055))),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
