# Generated by Django 3.1.13 on 2022-03-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0042_auto_20211229_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='input',
            field=models.CharField(db_index=True, max_length=512, verbose_name='Input'),
        ),
        migrations.AlterField(
            model_name='command',
            name='output',
            field=models.TextField(blank=True, verbose_name='Output'),
        ),
    ]
