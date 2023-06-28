# Generated by Django 4.2.2 on 2023-06-23 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('my_user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('ctc', models.CharField(max_length=200, null=True)),
                ('stipend', models.CharField(max_length=200, null=True)),
                ('company_contact', models.CharField(blank=True, max_length=200, null=True)),
                ('additional_information', models.CharField(blank=True, max_length=500, null=True)),
                ('Role_offered', models.ManyToManyField(to='my_manager.role')),
                ('Spoc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_manager.coordinator')),
                ('hiring_who', models.ManyToManyField(to='my_manager.trade')),
            ],
        ),
    ]