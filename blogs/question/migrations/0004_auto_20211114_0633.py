# Generated by Django 3.2.8 on 2021-11-14 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_auto_20211114_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='mentor_response',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='query',
            name='query_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
