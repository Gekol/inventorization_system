# Generated by Django 4.0.4 on 2022-05-08 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('analytics_service', '0001_initial'),
        ('inventorization_service', '0006_alter_item_fix_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    to='analytics_service.itemtype'),
        ),
    ]
