from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import Event , Person

# Create your views here.
def home(request):
    event_list = Event.objects.order_by('event_name')
    context = {'event_list': event_list}
    return render(request, 'event/home.html', context)


def new_event(request):
    event = Event.objects.all()
    if request.method == 'POST':
        if request.POST['name'] == "":
            return render(request, 'event/create_event.html', {'event': event, 'error_msg':"Please input Event Name"},)
        else:
            Event.objects.create(event_name=request.POST['name'], event_detail=request.POST['detail'],
                event_numset=request.POST['numset'], event_location=request.POST['location'], pcount=0,)
        return HttpResponseRedirect(reverse('event:home',))


    return render(request, 'event/create_event.html', {'event': event},)


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.person_set.create(fname=request.POST['firstname'], lname=request.POST['lastname'])
        event.pcount += 1
        event.save()
        return HttpResponseRedirect(reverse('event:event_detail',args=(event.id,)))

    return render(request, 'event/detail.html', {'event':event},)

def sign_name(request, event_id):
    pass
    #return HttpResponseRedirect(reverse('event_detail',kwargs={'event_id':event_id}))
        #return HttpResponseRedirect(reverse('event:event_detail',args=(event.id,)))

def delete_name(request, event_id):    #, person_id
    event = get_object_or_404(Event, pk=event_id)
    person_name = event.person_set.get(pk=request.POST['del_btn'])#request.POST['del_btn']
    person_name.delete()
    event.pcount -= 1
    event.save()
    return HttpResponseRedirect(reverse('event:event_detail',args=(event.id,)))

def delete_event(request):
    password = "delete"
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=request.POST['numdel'])
        #id_event = Event.objects.get(pk=request.POST['numdel'])

        #check_event_id = Event.objects.filter(id=event)
        pw = request.POST['pw']
        if (pw == password) :
            event.delete()

        else:
            pass
    return HttpResponseRedirect(reverse('event:homeadmin',))

    '''password = "delete"
    if request.method == 'POST':
        #event = get_object_or_404(Event, pk=request.POST['numdel'])
        id_event = Event.objects.get(pk=request.POST['numdel'])

        check_event_id = Event.objects.filter(id=id_event)
        pw = request.POST['pw']
        if check_event_id and (pw == password) :
            event.delete()

        else:
            pass
    return HttpResponseRedirect(reverse('event:home',))'''


    '''event = get_object_or_404(Event, pk=request.POST['numdel'])
    password = "delete"
    if request.method == 'POST':
        pw = request.POST['pw']
        if pw == password:
            try:
                event.delete()
            except:
                pass
        else:
            pass
    return HttpResponseRedirect(reverse('event:home',))'''
def login_page(request):
    return render(request, 'login.html','')



def login_r(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        #return HttpResponseRedirect(reverse('event:homeadmin',))
        return HttpResponseRedirect('/adminhome')
        #return HttpResponseRedirect('/login_success')
    else:
        return HttpResponseRedirect('/login_page')


@login_required(login_url='event:login_page')
def login_success(request):
    return render(request, 'loginsuccess.html','')


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login_page')



@login_required(login_url='event:login_page')
def admin_home(request):
    event_list = Event.objects.order_by('event_name')
    context = {'event_list': event_list}
    return render(request, 'event/homeadmin.html',context)

def about(request):
    return render(request, 'event/about.html','')