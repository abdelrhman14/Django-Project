# Generated by Django 3.2.9 on 2022-06-20 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_orderitem_qunatity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='qunatity',
            field=models.IntegerField(default=1),
        ),
    ]
