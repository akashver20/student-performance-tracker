# Generated by Django 4.2.6 on 2023-10-23 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='mobile',
            field=models.CharField(default='not provided', max_length=20),
            preserve_default=False,
        ),
    ]