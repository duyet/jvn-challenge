# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 14:33
from __future__ import unicode_literals

import competition.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0002_auto_20170429_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='label_col',
            field=models.CharField(default='label', max_length=250, verbose_name='Label column'),
        ),
        migrations.AddField(
            model_name='competition',
            name='sample_file',
            field=models.FileField(default=None, null=True, upload_to='sample_files', verbose_name='Sample file'),
        ),
        migrations.AddField(
            model_name='competition',
            name='validate_file',
            field=models.FileField(default=None, upload_to='validate_files', verbose_name='Validation file'),
        ),
        migrations.AlterField(
            model_name='competitionsubmit',
            name='file',
            field=models.FileField(upload_to='submit_file', validators=[competition.utils.FileValidator(content_types=('text/csv', 'text/plain', 'application/vnd.ms-excel'), max_size=104857600)]),
        ),
    ]