# Generated by Django 3.0 on 2021-03-12 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='addr',
            field=models.CharField(blank=True, db_column='address', max_length=100, null=True, verbose_name='address'),
        ),
    ]