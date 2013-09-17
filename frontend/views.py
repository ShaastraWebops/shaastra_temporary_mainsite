# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from misc.dajaxice.core import dajaxice_functions

def home(request):
    return render_to_response ('home/home.html', locals(), context_instance=RequestContext(request))
from misc.dajaxice.core import dajaxice_functions

def serenity(request):
    return render_to_response ('index.html', locals(), context_instance=RequestContext(request))
