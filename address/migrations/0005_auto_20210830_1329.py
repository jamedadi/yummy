# Generated by Django 3.2 on 2021-08-30 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_auto_20210830_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraddress',
            name='alley',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='street',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='serviceaddress',
            name='alley',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='serviceaddress',
            name='street',
            field=models.CharField(max_length=50),
        ),
    ]
