# Generated by Django 5.1.5 on 2025-01-28 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0005_alter_blog_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='comments',
            field=models.TextField(blank=True, max_length=600, null=True),
        ),
    ]
