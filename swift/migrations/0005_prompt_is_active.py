# Generated by Django 5.0.6 on 2024-05-24 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swift', '0004_prompt_promptoutput'),
    ]

    operations = [
        migrations.AddField(
            model_name='prompt',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
