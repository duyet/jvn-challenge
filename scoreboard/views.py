# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from accounts.models import User

def index(request):
	users = User.objects.all()
	context = {
		"users": users
	}
	return render(request, 'scoreboard/index.html', context)