# Generated by Django 3.0.8 on 2020-08-11 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0019_rating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rating',
        ),
    ]