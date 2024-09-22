# Generated by Django 5.1.1 on 2024-09-21 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('autism_image', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autism_Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('results_id', models.IntegerField()),
                ('result', models.CharField(max_length=80)),
                ('updated_at', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autism_image.autism_image')),
            ],
        ),
    ]
