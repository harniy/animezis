# Generated by Django 3.0.8 on 2020-08-13 08:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0020_delete_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'ordering': ('name',), 'verbose_name': 'Актеры и режиссеры', 'verbose_name_plural': 'Актеры и режиссеры'},
        ),
        migrations.AddField(
            model_name='movie',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]