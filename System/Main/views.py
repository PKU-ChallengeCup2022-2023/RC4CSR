from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect

# Create your views here.
def index(request: HttpRequest):
    if request.user:
        return render(request, 'index.html', locals())
    else:
        return HttpResponseRedirect('/account/login')