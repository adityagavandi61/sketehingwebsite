# Generated by Django 3.2.25 on 2024-09-23 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_addcart_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='created_at',
        ),
    ]
