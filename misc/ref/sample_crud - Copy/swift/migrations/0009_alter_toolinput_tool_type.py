# Generated by Django 5.0.6 on 2024-05-28 16:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swift', '0008_inputtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolinput',
            name='tool_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='input_type', to='swift.inputtype'),
        ),
    ]