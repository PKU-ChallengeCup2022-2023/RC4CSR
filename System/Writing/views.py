from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
import datetime

from .models import Pencraft, Chapter
from Account.models import PlatformUser

@login_required(redirect_field_name='login')
def index(request):
    platform_user = PlatformUser.objects.get(uid=request.user)
    pencraft_list = Pencraft.objects.order_by('-pub_date')
    return render(request, 'Writing/index.html', locals())

@login_required(redirect_field_name='login')
def pencraft(request, pencraft_id):
    platform_user = PlatformUser.objects.get(uid=request.user)
    pencraft = get_object_or_404(Pencraft, pk=pencraft_id)
    chapter_set = Chapter.objects.filter(collection=pencraft)
    return render(request, 'Writing/pencraft.html', locals())

@login_required(redirect_field_name='login')
def chapter(request, pencraft_id, chapter_id):
    platform_user = PlatformUser.objects.get(uid=request.user)
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    return render(request, 'Writing/chapter.html', locals())

@login_required(redirect_field_name='login')
def author(request, username):
    user = User.objects.get(username=username)
    platform_user = PlatformUser.objects.get(uid=user)
    pencraft_list = Pencraft.objects.filter(author=platform_user)
    
    if request.method == "POST" and request.POST:
        topic = request.POST["topic"]
        description = request.POST["description"]
        try:
            pencraft_new = Pencraft.objects.create(
                topic=topic,
                chap_num=0,
                description=description,
                pub_date=datetime.datetime.today(),
                author=PlatformUser.objects.get(uid=request.user),
            )
            err_msg = "发布成功！"
        except:
            print("Something is wrong when the user start a new pencraft, uid=", request.user)
            err_msg = "操作失败，请重试！"
            return render(request, 'Writing/author.html', locals())
    return render(request, 'Writing/author.html', locals())

@login_required(redirect_field_name='login')
def update(request, username):
    user = User.objects.get(username=username)
    platform_user = PlatformUser.objects.get(uid=user)
    pencraft_list = Pencraft.objects.filter(author=platform_user)
    
    if request.method == "POST" and request.POST:
        collection_id = request.POST["collection"]
        collection_update = Pencraft.objects.get(id=collection_id)
        chap_name = request.POST["chap_name"]
        text = request.POST["text"]
        try:
            collection_update.chap_num += 1
            collection_update.save()
            chap_new = Chapter.objects.create(
                collection=collection_update,
                order_num=collection_update.chap_num,
                chap_name=chap_name,
                text=text,
                pub_date=datetime.datetime.today(),
            )
            err_msg = "发布成功！"
        except:
            print("Something is wrong when the user start a new chapter, uid=", request.user)
            err_msg = "操作失败，请重试！"
            return render(request, 'Writing/update.html', locals())
        
    return render(request, 'Writing/update.html', locals())