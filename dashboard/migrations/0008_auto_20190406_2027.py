# Generated by Django 2.1.7 on 2019-04-07 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20190406_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.DeleteModel(
            name='Router',
        ),
    ]