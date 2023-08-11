# Generated by Django 4.1.4 on 2023-08-11 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_teacher_skill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='skill',
            field=models.IntegerField(blank=True, choices=[(1, 'Lecturer'), (2, 'Senior Lecturer'), (3, 'Assistant Professor'), (4, 'Associate Professor'), (5, 'Professor')], default=1, null=True),
        ),
    ]
