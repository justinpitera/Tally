# Generated by Django 5.0.1 on 2024-02-05 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursework', '0003_alter_course_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='syllabus',
            field=models.FileField(null=True, upload_to='submissions/%Y/%m/%d/'),
        ),
    ]
