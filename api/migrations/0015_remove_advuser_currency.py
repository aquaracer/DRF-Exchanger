# Generated by Django 3.1.1 on 2020-09-03 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20200903_2356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advuser',
            name='currency',
        ),
    ]
