# Generated by Django 4.0.3 on 2022-03-27 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('reg_number', models.CharField(max_length=12, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('other_names', models.CharField(max_length=255)),
                ('level_of_study', models.IntegerField(blank=True, null=True)),
                ('fingerprint_template', models.CharField(max_length=512)),
            ],
        ),
    ]
