from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_world(request):

    if 'MY-APPLICATION-MESSAGE' in request.headers:
        message = request.headers['MY-APPLICATION-MESSAGE']
    else:
        message = request.GET.get('message', 'Hello World!')
    return HttpResponse(message)
