# Generated by Django 3.0 on 2021-03-13 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20210312_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='discount',
            field=models.DecimalField(db_column='discount', decimal_places=2, max_digits=4, verbose_name='discount'),
        ),
    ]
