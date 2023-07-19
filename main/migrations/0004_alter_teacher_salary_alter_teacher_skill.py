# Generated by Django 4.1.4 on 2023-07-19 21:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_class_name_alter_subject_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='salary',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(999999)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='skill',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
