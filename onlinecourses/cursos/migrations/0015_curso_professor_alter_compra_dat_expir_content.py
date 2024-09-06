# Generated by Django 4.1.7 on 2023-05-11 18:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0014_alter_compra_dat_expir'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='professor',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='cursos.professor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='compra',
            name='dat_expir',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 11, 18, 52, 8, 130543, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='contents/')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursos.curso')),
            ],
        ),
    ]
