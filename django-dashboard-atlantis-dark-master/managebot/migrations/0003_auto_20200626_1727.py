# Generated by Django 3.0.7 on 2020-06-26 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managebot', '0002_auto_20200626_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custom_command',
            name='guild_name',
            field=models.CharField(max_length=100),
        ),
    ]
