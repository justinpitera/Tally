# Generated by Django 5.0.1 on 2024-02-07 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinelearning', '0004_module_end_date_module_start_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Media',
        ),
        migrations.DeleteModel(
            name='Text',
        ),
        migrations.DeleteModel(
            name='URL',
        ),
        migrations.DeleteModel(
            name='UserContent',
        ),
    ]
