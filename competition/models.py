# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models import Max, F
from django.utils import timezone
from django.dispatch import receiver
from django.utils.timezone import now
from tinymce import models as tinymce_models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible

from .utils import *

@python_2_unicode_compatible  # only if you need to support Python 2
class Competition(models.Model):
    add_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    datasets = models.ManyToManyField(
        "competition.CompetitionDataset",
        blank=True
    )

    title = models.CharField("Competition title", max_length=250)
    content = tinymce_models.HTMLField('Competition content') # models.TextField("Competition content")
    prizes = tinymce_models.HTMLField("Competition prizes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField("Deadline")
    
    # Auto score
    validate_file = models.FileField("Validation file", upload_to='validate_files', null=False, default="")
    label_col = models.CharField("Label column", max_length=250, default="label")
    id_col = models.CharField("ID column", max_length=250, default="id")
    sample_file = models.FileField("Sample file", upload_to='sample_files', null=True, default=None)

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

validate_file = FileValidator(max_size=1024 * 1024 * 10, 
        content_types=('text/csv', 'text/plain', 'application/vnd.ms-excel'))
@python_2_unicode_compatible
class CompetitionSubmit(models.Model):
    competition = models.ForeignKey(
        Competition,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    score = models.FloatField("Score", default=0)

    file = models.FileField(upload_to='submit_file', validators=[validate_file])
    status = models.CharField("Status of submission", default="unknown", max_length=150)
    message = models.CharField("Message", default="", max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"Submit of %s to #%s" % (self.author, self.competition.id)

    def get_ranking_list(self, competition_id=-1):
        return CompetitionSubmit.objects \
            .order_by("-score", "-created_at") \
            .filter(competition=competition_id, status='success')

@receiver(post_save, sender=CompetitionSubmit, dispatch_uid="checking_score_from_submit_file")
def checking_score_from_submit_file(sender, instance, **kwargs):
    if instance.status == 'unknown' and instance.message == '':
        validate = validate_score(instance.file, 
                instance.competition.validate_file, 
                label_col=instance.competition.label_col,
                id_col=instance.competition.id_col)
        instance.score = validate['score']
        instance.status = validate['status']
        instance.message = validate['message']
        instance.save()