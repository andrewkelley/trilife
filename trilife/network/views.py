from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from network.models import Member
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from network.forms import LoginForm
from django.contrib.auth import authenticate, login, logout

def index(request):
    member = Member.objects.all()
    return render_to_response('index.html', { member:'member' }, context_instance=RequestContext(request))

def LoginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/index/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                return render_to_response('trilife/index.html', {'form':form}, context_instance=RequestContext(request))
        else:
            return render_to_response('trilife/index.html', {'form':form}, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        context = {'form':form}
        return render_to_response('trilife/index.html', {'form':form}, context, context_instance=RequestContext(request))
