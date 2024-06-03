# Generated by Django 5.0.6 on 2024-06-02 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swift', '0009_alter_toolinput_tool_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputtype',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('email', 'Email'), ('textarea', 'Textarea')], max_length=150),
        ),
    ]
