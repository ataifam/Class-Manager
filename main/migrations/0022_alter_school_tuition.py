# Generated by Django 4.1.4 on 2023-08-22 16:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_school_money_school_tuition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='tuition',
            field=models.IntegerField(blank=True, default=50000, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)]),
        ),
    ]
