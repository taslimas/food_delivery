# Generated by Django 4.1.3 on 2022-12-24 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_food_quantity_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product',
            new_name='food',
        ),
    ]