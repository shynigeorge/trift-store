# Generated by Django 4.0 on 2024-03-05 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0036_alter_order_products'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
