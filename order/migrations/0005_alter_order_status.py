# Generated by Django 3.2 on 2021-09-13 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'preparing food'), (1, 'sending'), (2, 'delivered')], default=0, verbose_name='status'),
        ),
    ]
