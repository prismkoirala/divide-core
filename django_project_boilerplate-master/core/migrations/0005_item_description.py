# Generated by Django 2.2 on 2019-07-12 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='This is a dummy description'),
            preserve_default=False,
        ),
    ]
