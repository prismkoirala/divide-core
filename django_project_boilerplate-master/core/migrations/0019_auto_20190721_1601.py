# Generated by Django 2.2 on 2019-07-21 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20190721_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='add_image1',
            field=models.ImageField(blank=True, default='default/add_default.jpg', null=True, upload_to='additional/'),
        ),
        migrations.AddField(
            model_name='item',
            name='add_image2',
            field=models.ImageField(blank=True, default='default/add_default.jpg', null=True, upload_to='additional/'),
        ),
        migrations.AddField(
            model_name='item',
            name='add_image3',
            field=models.ImageField(blank=True, default='default/add_default.jpg', null=True, upload_to='additional/'),
        ),
        migrations.AddField(
            model_name='item',
            name='add_info',
            field=models.TextField(default=' DUMMY ADDITINAL INFO'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default='default/default-dummy-image.jpg', null=True, upload_to='product-img/'),
        ),
    ]