# Generated by Django 3.2.9 on 2021-11-13 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
