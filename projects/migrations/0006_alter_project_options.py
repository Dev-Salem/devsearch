# Generated by Django 5.0.6 on 2024-06-09 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_options_review_owner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ration', '-total_votes', 'title']},
        ),
    ]