# Generated by Django 4.1.4 on 2023-07-27 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_school_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(default='My New School', max_length=30),
        ),
    ]
