# Generated by Django 3.2.25 on 2024-08-27 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='p_id',
            new_name='product',
        ),
    ]
