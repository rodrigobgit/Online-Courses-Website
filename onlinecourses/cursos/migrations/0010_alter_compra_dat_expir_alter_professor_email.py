# Generated by Django 4.1.7 on 2023-05-11 18:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0009_professor_email_alter_compra_dat_expir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='dat_expir',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 11, 18, 15, 27, 512562, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='professor',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]