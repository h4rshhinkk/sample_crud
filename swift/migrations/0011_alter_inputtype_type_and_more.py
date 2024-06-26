# Generated by Django 5.0.6 on 2024-06-03 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swift', '0010_alter_inputtype_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputtype',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('email', 'Email'), ('textarea', 'Textarea')], max_length=50),
        ),
        migrations.AlterField(
            model_name='tooltemplateinput',
            name='sort_order',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='tooltemplateinput',
            name='validation_message',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
