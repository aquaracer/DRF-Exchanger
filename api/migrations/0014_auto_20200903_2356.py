# Generated by Django 3.1.1 on 2020-09-03 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20200903_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
