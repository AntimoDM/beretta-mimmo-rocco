# Generated by Django 5.0.1 on 2024-05-07 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_cliente_tecnicocaldaia_remove_customer_street_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cognome',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nome',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
