# Generated by Django 3.2.25 on 2024-09-23 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_remove_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='app.order'),
        ),
    ]
