# Generated by Django 5.0.6 on 2024-06-27 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_notic'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notic',
            new_name='Notice',
        ),
        migrations.AlterModelTable(
            name='notice',
            table='notice',
        ),
    ]