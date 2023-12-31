# Generated by Django 4.1.4 on 2023-08-11 17:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_class_user_alter_student_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='average_grade',
            field=models.CharField(default='C', max_length=1),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='skill',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1, null=True),
        ),
    ]
