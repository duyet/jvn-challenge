# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Competition, CompetitionDataset

admin.site.register(Competition)
admin.site.register(CompetitionDataset)