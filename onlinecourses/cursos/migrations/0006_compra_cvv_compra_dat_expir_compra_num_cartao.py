# Generated by Django 4.1.7 on 2023-05-09 23:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0005_remove_cliente_user_remove_professor_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='cvv',
            field=models.IntegerField(default=0, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compra',
            name='dat_expir',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 9, 23, 23, 37, 230818, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='compra',
            name='num_cartao',
            field=models.IntegerField(default=0, max_length=16),
            preserve_default=False,
        ),
    ]