# Generated by Django 4.2 on 2023-07-27 03:11

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_id', models.CharField(help_text='Store Subdomain', max_length=200, unique=True)),
                ('api_token', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.CharField(max_length=255)),
                ('line2', models.CharField(blank=True, max_length=255)),
                ('line3', models.CharField(blank=True, max_length=255)),
                ('line4', models.CharField(max_length=255, verbose_name='City')),
                ('state', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=64)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('ref_id', models.IntegerField(blank=True, help_text='External Reference ID', null=True)),
                ('name', models.CharField(max_length=255)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sku', models.CharField(max_length=255)),
                ('num_in_stock', models.IntegerField(default=0, help_text='Num Available')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.location')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store')),
            ],
            options={
                'unique_together': {('store', 'location', 'sku')},
            },
        ),
    ]