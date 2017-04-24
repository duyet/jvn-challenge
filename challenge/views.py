# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

def index(request):
	context = {}
	return render(request, 'challenge/index.html', context)

def about(request):
	context = {}
	return render(request, 'challenge/about.html', context)

def help(request):
	context = {}
	return render(request, 'challenge/help.html', context)

def resources(request):
	context = {}
	return render(request, 'challenge/resources.html', context)