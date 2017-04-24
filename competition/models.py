# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from tinymce import models as tinymce_models
from django.utils.timezone import now

@python_2_unicode_compatible  # only if you need to support Python 2
class Competition(models.Model):
    add_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    datasets = models.ManyToManyField(
        "competition.CompetitionDataset",
        blank=True,
        null=True
    )

    title = models.CharField("Competition title", max_length=250)
    content = tinymce_models.HTMLField('Competition content') # models.TextField("Competition content")
    prizes = tinymce_models.HTMLField("Competition prizes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField("Deadline")
    
    def is_deadline(self):
    	return now() > self.deadline

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class CompetitionDataset(models.Model):
    file_name = models.CharField("File name", max_length=200)
    download_count = models.IntegerField("Counter", default = 0)
    file = models.FileField(upload_to='dataset')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name