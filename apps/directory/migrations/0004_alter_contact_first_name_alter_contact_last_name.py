# Generated by Django 5.2.3 on 2025-06-20 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0003_alter_contact_options_remove_contact_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Apellido'),
        ),
    ]
