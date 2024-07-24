# Generated by Django 4.1.13 on 2024-07-09 10:19

from django.db import migrations


def migrate_platform_protocol_primary(apps, schema_editor):
    platform_model = apps.get_model('assets', 'Platform')
    platforms = platform_model.objects.all()

    for platform in platforms:
        p = platform.protocols.filter(primary=True).first()
        if p:
            continue
        p = platform.protocols.first()
        if not p:
            continue
        p.primary = True
        p.save()


class Migration(migrations.Migration):
    dependencies = [
        ('assets', '0003_auto_20180109_2331'),
    ]

    operations = [
        migrations.RunPython(migrate_platform_protocol_primary)
    ]