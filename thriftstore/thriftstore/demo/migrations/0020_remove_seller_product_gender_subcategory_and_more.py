# Generated by Django 5.0 on 2024-02-23 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0019_gender_sub_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller_product',
            name='gender_subcategory',
        ),
        migrations.DeleteModel(
            name='Gender_sub_category',
        ),
    ]