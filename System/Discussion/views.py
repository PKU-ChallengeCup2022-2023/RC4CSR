from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
import datetime
from django.contrib.auth.models import User, Group
from django.db.utils import IntegrityError
from django.utils import timezone
from Account.models import PlatformUser, PlatformUserManager
from Recommendation.models import Book
from .models import DiscGroup, DiscRecord, LikeRecord

# Create your views here.

@login_required(redirect_field_name="login")
def index(request):
    platform_user = PlatformUser.objects.get(uid=request.user)
    latest_group_list = DiscGroup.objects.order_by('-found_time')
    return render(request, 'Discussion/index.html', locals())

@login_required(redirect_field_name="login")
def detail(request: HttpRequest, group_id):
    group = get_object_or_404(DiscGroup, pk=group_id)
    records = DiscRecord.objects.filter(belong_to=group)
    platform_user = PlatformUser.objects.get(uid=request.user)
    
    if request.method == "POST" and request.POST:
        #TODO: likes & reply_to
        summary = request.POST["summary"]
        content = request.POST["content"]
        reply_to = request.POST["replyto"]
        try:
            disc_record = DiscRecord.objects.create(
                summary=summary,
                pub_time=datetime.datetime.now(),
                publisher=PlatformUser.objects.get(uid=request.user),
                belong_to=group,
		        reply_to=reply_to,
                content=content,
                like=LikeRecord.objects.create()
            )
            err_msg = "发布成功！"
        except:
            print("Something is wrong when the user discuss, uid=", request.user)
            err_msg = "操作失败，请重试！"
            return render(request, 'Discussion/detail.html', locals())

    return render(request, 'Discussion/detail.html', locals())

def check_same(name_list: list):
    """check_same
        Helper function for GroupRegister function
    """
    for i in range(len(name_list)-1):
        for j in range(i+1,len(name_list)):
            if name_list[i] and name_list[j] and name_list[i] == name_list[j]:
                return True
    return False

@login_required(redirect_field_name="login")
def GroupRegister(request: HttpRequest):
    platform_user = PlatformUser.objects.get(uid=request.user)
    if request.method == "POST" and request.POST:
        err_msg = "注册成功！"
        name = request.POST['name']
        bookname = request.POST['book']
        book = Book.objects.get(bookname=bookname)
        foundername = request.POST['founder']
        # Find the founder
        try:
            founder = PlatformUser.objects.get(uid=User.objects.get(username=foundername))
        except PlatformUser.DoesNotExist:
            err_msg = "发起者不存在！"
            return render(request, 'Discussion/register.html', locals())
        member1name = request.POST['member1']
        member2name = request.POST['member2']
        member3name = request.POST['member3']
        member4name = request.POST['member4']
        member5name = request.POST['member5']
        description = request.POST['description']

        if check_same([foundername, member1name, member2name, member3name, member4name, member5name]) == True:
            err_msg = "成员和发起者之间存在重复！"
            return render(request, 'Discussion/register.html', locals())

        # create base group
        try:
            group = Group.objects.create(name=name)
        except IntegrityError:
            err_msg="该组已存在！"
            return render(request, 'Discussion/register.html', locals())

        # create group
        try:
            discgroup = DiscGroup.objects.create(
                uid=group,
                groupName=name,
                disc_center=book,
                found_time=timezone.now(),
                founder=founder,
                description=description
            )
        except IntegrityError:
            err_msg="该组已存在！"
            group.delete()
            return render(request, 'Discussion/register.html', locals())

        # add member
        if member1name:
            try:
                discgroup.member1 = PlatformUser.objects.get(uid=User.objects.get(username=member1name))
            except PlatformUser.DoesNotExist:
                err_msg = "成员一不存在！"
                group.delete()
                discgroup.delete()
                return render(request, 'Discussion/register.html', locals())
        if member2name:
            try:
                discgroup.member2 = PlatformUser.objects.get(uid=User.objects.get(username=member2name))
            except PlatformUser.DoesNotExist:
                err_msg = "成员二不存在！"
                group.delete()
                discgroup.delete()
                return render(request, 'Discussion/register.html', locals())
        if member3name:
            try:
                discgroup.member3 = PlatformUser.objects.get(uid=User.objects.get(username=member3name))
            except PlatformUser.DoesNotExist:
                err_msg = "成员三不存在！"
                group.delete()
                discgroup.delete()
                return render(request, 'Discussion/register.html', locals())
        if member4name:
            try:
                discgroup.member4 = PlatformUser.objects.get(uid=User.objects.get(username=member4name))
            except PlatformUser.DoesNotExist:
                err_msg = "成员四不存在！"
                group.delete()
                discgroup.delete()
                return render(request, 'Discussion/register.html', locals())
        if member5name:
            try:
                discgroup.member5 = PlatformUser.objects.get(uid=User.objects.get(username=member5name))
            except PlatformUser.DoesNotExist:
                err_msg = "成员五不存在！"
                group.delete()
                discgroup.delete()
                return render(request, 'Discussion/register.html', locals())
        discgroup.save()
        return render(request, 'Discussion/register.html', locals())
    else:
        return render(request, 'Discussion/register.html', locals())

@login_required(redirect_field_name='login')
def Like(request: HttpRequest, record_id):
    platform_user = PlatformUser.objects.get(uid=request.user)
    disc_record = get_object_or_404(DiscRecord, pk=record_id)
    group = disc_record.belong_to
    user_list = disc_record.like.like_users.all()
    if platform_user in user_list:
        disc_record.like.like_num -= 1
        disc_record.like.like_users.remove(platform_user)
    else:
        disc_record.like.like_num += 1
        disc_record.like.like_users.add(platform_user)
    disc_record.like.save()
    disc_record.save()
    return HttpResponseRedirect("/discussion/%s/" % group.id)
