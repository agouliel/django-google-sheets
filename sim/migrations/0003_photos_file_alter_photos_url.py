# Generated by Django 4.2.6 on 2023-11-15 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0002_photos_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='photos',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='.'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='url',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
