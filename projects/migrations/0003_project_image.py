# Generated by Django 5.0.6 on 2024-06-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_tag_project_total_votes_project_vote_ration_review_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]