# Generated by Django 4.0 on 2024-03-05 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('demo', '0038_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=10)),
                ('district', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Courier_Assign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateField(auto_now_add=True)),
                ('delivery_date', models.DateField(auto_now_add=True)),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.courier')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.order')),
            ],
        ),
    ]
