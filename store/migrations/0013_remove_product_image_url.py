# Generated by Django 5.1.2 on 2024-10-22 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_shopreviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
    ]
