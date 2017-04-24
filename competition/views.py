# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os 
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Competition, CompetitionDataset
from django.core.files import File

def index(request):
	list_competitions = Competition.objects.order_by('-created_at')[:15]
	context = {
		"user": request.user,
		"list_competitions": list_competitions
	}
	return render(request, 'competition/index.html', context)

def detail(request, id=0):
	competition = get_object_or_404(Competition, pk=id)

	context = {
		"user": request.user,
		"competition": competition
	}
	return render(request, 'competition/detail.html', context)

def dataset(request):
	list_datasets = CompetitionDataset.objects.order_by('-created_at')[:15]
	context = {
		"user": request.user,
		"list_datasets": list_datasets
	}
	return render(request, 'competition/datasets.html', context)

def submit(request, id = 0):
	competition = get_object_or_404(Competition, pk=id)
	
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	context = {
		"user": request.user,
	}
	return render(request, 'competition/submit.html', context)

def download(request, id):
    file = get_object_or_404(CompetitionDataset, pk=id)
    file.download_count += 1
    file.save()

    filename = file.file.name.split('/')[-1]
    response = HttpResponse(file.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response
