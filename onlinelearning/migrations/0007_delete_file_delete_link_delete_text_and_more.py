# Generated by Django 5.0.1 on 2024-02-07 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinelearning', '0006_file_link_text_usercontent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='Link',
        ),
        migrations.DeleteModel(
            name='Text',
        ),
        migrations.DeleteModel(
            name='UserContent',
        ),
    ]
