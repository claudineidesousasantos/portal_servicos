# Generated by Django 5.0.6 on 2024-06-21 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='barbearias',
            field=models.ManyToManyField(related_name='clientes', to='portal.barbearia'),
        ),
    ]
