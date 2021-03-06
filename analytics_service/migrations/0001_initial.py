# Generated by Django 4.0.4 on 2022-05-08 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('min_amount', models.IntegerField(default=3)),
                ('is_permanent', models.BooleanField(default=False)),
            ],
        ),
    ]
