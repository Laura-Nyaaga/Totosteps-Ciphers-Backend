# Generated by Django 4.2.16 on 2024-09-23 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('milestones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField(unique=True)),
                ('correct_answer', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], max_length=3)),
                ('question_type', models.CharField(choices=[('multiple choice', 'Multiple Choice'), ('open-ended', 'Open-Ended')], max_length=25)),
                ('category', models.CharField(choices=[('Social', 'Social'), ('Language', 'Language'), ('Cognitive', 'Cognitive'), ('Movement', 'Movement')], max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='milestones.milestone')),
            ],
        ),
    ]
