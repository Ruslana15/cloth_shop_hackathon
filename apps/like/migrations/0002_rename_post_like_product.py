# Generated by Django 3.2.5 on 2022-11-29 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('like', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='post',
            new_name='product',
        ),
    ]
