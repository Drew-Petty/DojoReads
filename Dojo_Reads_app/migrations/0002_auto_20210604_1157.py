# Generated by Django 3.1.7 on 2021-06-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dojo_Reads_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
