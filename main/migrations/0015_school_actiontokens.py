# Generated by Django 4.1.4 on 2023-08-09 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_school_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='actionTokens',
            field=models.IntegerField(default=3),
        ),
    ]