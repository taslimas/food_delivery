# Generated by Django 4.1.3 on 2023-02-06 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0010_alter_orderplaced_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.customer'),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.food'),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
