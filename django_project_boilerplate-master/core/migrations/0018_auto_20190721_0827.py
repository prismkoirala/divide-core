# Generated by Django 2.2 on 2019-07-21 02:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0017_order_billing_address'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BillingAddress',
            new_name='BillingAddresse',
        ),
    ]
