# Generated by Django 3.2 on 2021-06-19 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Toys', '0015_alter_order_productscode'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
