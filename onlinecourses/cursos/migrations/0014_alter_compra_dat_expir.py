# Generated by Django 4.1.7 on 2023-05-11 18:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0013_alter_compra_dat_expir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='dat_expir',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 11, 18, 21, 7, 510237, tzinfo=datetime.timezone.utc)),
        ),
    ]
