# Generated by Django 4.1.4 on 2023-08-08 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_subject_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]