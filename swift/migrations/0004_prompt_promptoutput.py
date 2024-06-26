# Generated by Django 5.0.6 on 2024-05-24 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swift', '0003_rename_curriculam_curriculum_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PromptOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.JSONField(default=dict)),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prompt', to='swift.prompt')),
            ],
        ),
    ]
