from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from network.models import Member

def index(request):
    member = Member.objects.all()
    return render_to_response('trilife/index.html', { member:'member' })
