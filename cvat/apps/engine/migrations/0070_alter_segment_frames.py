# Generated by Django 3.2.18 on 2023-04-10 19:07

import cvat.apps.engine.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0069_annotationconflict_annotationconflictsreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='segment',
            name='frames',
            field=cvat.apps.engine.models.IntArrayField(blank=True, default=''),
        ),
    ]