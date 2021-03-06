# Generated by Django 2.1.5 on 2019-04-21 20:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmartHomeDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('image', models.ImageField(blank=True, null=True, upload_to='device-pictures')),
            ],
        ),
        migrations.AddField(
            model_name='datafile',
            name='processed_file',
            field=models.FileField(blank=True, null=True, upload_to='media/data-files', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])]),
        ),
        migrations.AlterField(
            model_name='datafile',
            name='data_file',
            field=models.FileField(upload_to='media/data-files', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pcap'])]),
        ),
        migrations.AddField(
            model_name='datafile',
            name='devices_captured',
            field=models.ManyToManyField(to='api.SmartHomeDevice'),
        ),
    ]
