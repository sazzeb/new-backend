# Generated by Django 3.2.11 on 2022-01-17 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_merge_0004_auto_20211214_1343_0004_auto_20220117_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='education',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_answers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_downvotes',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_questions',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_upvotes',
        ),
    ]