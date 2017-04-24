# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings


@python_2_unicode_compatible  # only if you need to support Python 2
class Submit(models.Model):
    challenge_name = models.CharField(max_length=200)
    submited_date = models.DateTimeField('submited date', editable=False)
    last_updated = models.DateTimeField('last update')
    number_of_submit = models.CharField(max_length=200)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.submited_date = timezone.now()
            self.number_of_submit = 0
        self.last_updated = timezone.now()
        self.number_of_submit = self.number_of_submit + 1
        return super(Submit, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + '-' + str(self.challenge_name)