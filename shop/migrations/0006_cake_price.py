# Generated by Django 4.0.5 on 2022-06-16 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_orderc_price_remove_orderc_weight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cake',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]