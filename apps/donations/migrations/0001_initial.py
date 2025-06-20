# Generated by Django 5.2.3 on 2025-06-17 21:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre del tipo de donación')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Título')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Monto')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('method', models.CharField(blank=True, choices=[('deposito', 'Depósito bancario'), ('transferencia', 'Transferencia electrónica'), ('relaciones_publicas', 'Mesa de Relaciones Públicas'), ('ministerio', 'Encargado de Ministerio'), ('entrega_directa', 'Entrega directa en instalaciones')], max_length=100, null=True, verbose_name='Método de pago')),
                ('entity', models.CharField(blank=True, max_length=100, null=True, verbose_name='Entidad')),
                ('bank', models.CharField(blank=True, max_length=100, null=True, verbose_name='Banco')),
                ('clabe', models.CharField(blank=True, max_length=50, null=True, verbose_name='CLABE')),
                ('location', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ubicación')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('donation_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='donations.donationtype', verbose_name='Tipo de donación')),
            ],
            options={
                'verbose_name': 'Donación',
                'verbose_name_plural': 'Donaciones',
                'ordering': ['-created_at'],
            },
        ),
    ]
