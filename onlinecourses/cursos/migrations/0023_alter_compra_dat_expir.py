# Generated by Django 4.1.7 on 2023-05-11 19:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0022_alter_compra_dat_expir_alter_curso_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='dat_expir',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 11, 19, 41, 16, 54393, tzinfo=datetime.timezone.utc)),
        ),
    ]
