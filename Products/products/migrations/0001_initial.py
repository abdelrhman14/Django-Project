# Generated by Django 3.2.9 on 2022-06-17 23:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brands', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CATname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Category Name')),
                ('CATdescription', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
                ('slug', models.SlugField(blank=True, null=True, verbose_name='Slug')),
                ('CATparent', models.ForeignKey(blank=True, limit_choices_to={'CATparent__isnull': True}, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='Category Parent')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PRname', models.CharField(blank=True, max_length=250, null=True, verbose_name='Product Name')),
                ('PRdescription', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('pr_code', models.CharField(blank=True, max_length=250, null=True, verbose_name='Product Code')),
                ('PRprice', models.FloatField(blank=True, null=True, verbose_name='Price')),
                ('PRdiscount_price', models.FloatField(blank=True, null=True, verbose_name='Discount Price')),
                ('PRstate', models.BooleanField(blank=True, null=True, verbose_name='is_active')),
                ('PRimage', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Image')),
                ('PRnp_available', models.IntegerField(blank=True, null=True, verbose_name='Number Available')),
                ('PRnew', models.BooleanField(default=True, verbose_name='New | Not')),
                ('PRbestseller', models.BooleanField(default=False, verbose_name='Bestseller | Not')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brands.brands', verbose_name='Brands')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ShippingAddress',
                'verbose_name_plural': 'ShippingAddress',
            },
        ),
        migrations.CreateModel(
            name='ProductsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='images/', verbose_name='Image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.products')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='Product_Alternative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlaneA_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_product', to='products.products')),
                ('PlaneB_product', models.ManyToManyField(related_name='alternative_product', to='products.Products')),
            ],
            options={
                'verbose_name': 'Product alternative',
                'verbose_name_plural': 'Product alternatives',
            },
        ),
        migrations.CreateModel(
            name='Product_Accessories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlaneA_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_Accessories', to='products.products')),
                ('PlaneB_PRODUCT', models.ManyToManyField(related_name='accessories_product', to='products.Products')),
            ],
            options={
                'verbose_name': 'Product Accessory',
                'verbose_name_plural': 'Product Accessories',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qunatity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'OrderItems',
                'verbose_name_plural': 'OrderItemss',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='products.OrderItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
