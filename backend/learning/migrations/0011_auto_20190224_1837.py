# Generated by Django 2.1.5 on 2019-02-24 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0010_auto_20190224_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
