# Generated by Django 3.2.9 on 2022-06-23 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_comment_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='items', to='products.OrderItem'),
        ),
    ]
