# Generated by Django 4.2 on 2023-08-30 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='products/'),
        ),
    ]
