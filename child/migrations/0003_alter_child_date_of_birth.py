# Generated by Django 4.2.16 on 2024-09-24 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('child', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='child',
            name='date_of_birth',
            field=models.DateTimeField(),
        ),
    ]