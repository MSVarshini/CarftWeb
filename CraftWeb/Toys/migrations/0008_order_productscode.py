# Generated by Django 3.2 on 2021-06-17 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Toys', '0007_remove_order_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='productscode',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]