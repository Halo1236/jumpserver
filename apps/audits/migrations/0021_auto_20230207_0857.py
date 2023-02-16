# Generated by Django 3.2.16 on 2023-02-07 00:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('audits', '0020_auto_20230117_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('O', 'Operate log'), ('S', 'Session log'), ('L', 'Login log'), ('T', 'Task')], default=None, max_length=2, null=True, verbose_name='Activity type')),
                ('resource_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Resource')),
                ('datetime', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Datetime')),
                ('detail', models.TextField(blank=True, default='', verbose_name='Detail')),
                ('detail_id', models.CharField(default=None, max_length=36, null=True, verbose_name='Detail ID')),
            ],
            options={
                'verbose_name': 'Activity log',
                'ordering': ('-datetime',),
            },
        ),
    ]