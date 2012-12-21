from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from network.models import Member
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from network.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
import trilife.settings as settings
import stripe

def index(request):
    member = Member.objects.all()
    return render_to_response('index.html', { member:'member' }, context_instance=RequestContext(request))

def received(request):
    member = Member.objects.all()
    return render_to_response('received.html', {member:'member'}, context_instance=RequestContext(request))

def payment(request):
    user = request.user
    member = Member.objects.get(user=user)
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET
        token = request.POST['stripeToken']
        customer = stripe.Customer.create(
            card=token,
            email=member.email
        )

        member.stripe_id = customer.id        
        member.save()
        
        charge = stripe.Charge.create(
            amount=1000,
            currency="usd",
            customer=customer.id
        )

        return HttpResponseRedirect('/received')
    else:
        member = Member.objects.all()
        return render_to_response('payment.html', { member:'member' }, context_instance=RequestContext(request))

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
                return render_to_response('index.html', {'form':form}, context_instance=RequestContext(request))
        else:
            return render_to_response('index.html', {'form':form}, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        context = {'form':form}
        return render_to_response('index.html', {'form':form}, context_instance=RequestContext(request))
