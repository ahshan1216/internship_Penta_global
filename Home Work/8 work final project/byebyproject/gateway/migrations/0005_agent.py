# Generated by Django 5.0.6 on 2025-05-15 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateway', '0004_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('client_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gateway.client')),
            ],
            bases=('gateway.client',),
        ),
    ]
