# Generated by Django 4.0.6 on 2022-08-02 13:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('listing_id', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('building', models.CharField(blank=True, max_length=255, null=True)),
                ('district', models.CharField(blank=True, max_length=255, null=True)),
                ('neighborhood', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('beds', models.FloatField(blank=True, null=True)),
                ('baths', models.IntegerField(blank=True, null=True)),
                ('surface', models.FloatField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('highlights', models.TextField(blank=True, null=True)),
                ('furnishing', models.CharField(blank=True, max_length=255, null=True)),
                ('amenities', models.TextField(blank=True, null=True)),
                ('completion_year', models.CharField(blank=True, max_length=255, null=True)),
                ('floor', models.CharField(blank=True, max_length=255, null=True)),
                ('views', models.IntegerField(blank=True, null=True)),
                ('discounted', models.IntegerField(blank=True, null=True)),
                ('cheap', models.IntegerField(blank=True, null=True)),
                ('distressed', models.IntegerField(blank=True, null=True)),
                ('investment', models.IntegerField(blank=True, null=True)),
                ('tenanted', models.IntegerField(blank=True, null=True)),
                ('vacant', models.IntegerField(blank=True, null=True)),
                ('metro', models.IntegerField(blank=True, null=True)),
                ('furnished', models.IntegerField(blank=True, null=True)),
                ('condition', models.IntegerField(blank=True, null=True)),
                ('upgraded', models.CharField(blank=True, max_length=255, null=True)),
                ('luxury', models.IntegerField(blank=True, null=True)),
                ('price_sqf', models.FloatField(blank=True, null=True)),
                ('median_sqf', models.FloatField(blank=True, null=True)),
                ('diff_percent', models.FloatField(blank=True, null=True)),
                ('valuation', models.CharField(blank=True, max_length=255, null=True)),
                ('featured_image', models.ImageField(blank=True, default='', null=True, upload_to='')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'db_table': 'ready_flats',
                'managed': False,
            },
        ),
    ]
