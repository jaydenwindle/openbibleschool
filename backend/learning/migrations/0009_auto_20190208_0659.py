# Generated by Django 2.1.5 on 2019-02-08 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0008_video_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.DurationField(),
        ),
    ]
