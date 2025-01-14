# Generated by Django 5.0 on 2024-01-19 11:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0014_customer_dob'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='district',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='housename',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_seller',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='landmark',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='state',
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_seller', models.BooleanField(default=False)),
                ('housename', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=80)),
                ('pincode', models.CharField(max_length=6)),
                ('landmark', models.CharField(max_length=100, null=True)),
                ('district', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
