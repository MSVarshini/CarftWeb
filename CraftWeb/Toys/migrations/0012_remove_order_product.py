# Generated by Django 3.2 on 2021-06-18 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Toys', '0011_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]
