# Generated by Django 3.1.1 on 2020-09-04 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_remove_advuser_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='advuser',
            name='currency',
            field=models.ForeignKey(blank=True, default='USD', on_delete=django.db.models.deletion.PROTECT, to='api.currency', to_field='short_name'),
        ),
    ]