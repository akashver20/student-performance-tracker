# Generated by Django 4.2.6 on 2023-10-25 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GradeWise', '0002_delete_teacher'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Class',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
    ]
