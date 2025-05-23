# Generated by Django 5.2 on 2025-04-29 05:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreCoffe', '0003_alter_usuario_options_alter_usuario_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('commerce_code', models.CharField(max_length=100)),
                ('monto', models.FloatField()),
                ('id_session', models.CharField(max_length=100)),
                ('estado', models.CharField(default='pendiente', max_length=20)),
            ],
        ),
    ]
