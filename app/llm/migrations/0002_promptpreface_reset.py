# Generated by Django 5.0.6 on 2024-08-15 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promptpreface',
            name='reset',
            field=models.BooleanField(default=False, help_text='reset the formatting, instruction'),
        ),
    ]
