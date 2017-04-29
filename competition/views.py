# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
import os 
import pandas as pd
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Competition, CompetitionDataset, CompetitionSubmit
from .forms import CompetitionSubmitForm
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
    
    your_submited = None
    if request.user.is_authenticated:
        your_submited = CompetitionSubmit.objects \
            .filter(competition=competition, author=request.user) \
            .order_by('-created_at')

    submit_ranking = CompetitionSubmit().get_ranking_list(id)

    context = {
        "user": request.user,
        "competition": competition,
        "your_submited": your_submited,
        "submit_ranking": submit_ranking
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


    if request.method == 'POST':
        form = CompetitionSubmitForm(request.user, competition, request.POST, request.FILES)
        print form
        if form.is_valid():
            form.save()
            return redirect(reverse('competition:detail', args=[id]) + '#Submit')
    else:
        form = CompetitionSubmitForm(request.user, competition)

    context = {
        "user": request.user,
        "form": form
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

def preview(request, id):
    file = get_object_or_404(CompetitionDataset, pk=id)
    
    try:
        df = pd.read_csv(file.file.path, nrows=20)
    except:
        return

    context = {
        'data_html': df.to_html(classes=['table table-bordered'], border=0),
        'file_name': file.file.name
    }

    return render(request, 'competition/preview_csv.html', context)

def preview_submit(request, id):
    file = get_object_or_404(CompetitionSubmit, pk=id)

    try:
        df = pd.read_csv(file.file.path, nrows=20)
    except:
        return

    context = {
        'data_html': df.to_html(classes=['table table-bordered'], border=0),
        'file_name': file.file.name
    }

    return render(request, 'competition/preview_csv.html', context)
