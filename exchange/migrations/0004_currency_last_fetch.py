# Generated by Django 2.2.6 on 2019-10-05 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_auto_20191004_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='last_fetch',
            field=models.DateField(blank=True, null=True),
        ),
    ]