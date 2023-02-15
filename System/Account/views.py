from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from .models import PlatformUser
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from Recommendation.models import Book_Tag

def check_password(password: str):
    """check password helper function
    return a list of error info
    """
    err_msg_pw = []
    try:
        validate_password(password)
    except ValidationError as e:
        for msg in e.messages:
            if msg == "This password is too short. It must contain at least 6 characters.":
                err_msg_pw.append("密码过短！合法的密码至少有6位！")
            elif msg == "This password is too common.":
                err_msg_pw.append("该密码太常见了！")
            elif msg == "This password is entirely numeric.":
                err_msg_pw.append("该密码是纯数字的！")
    return err_msg_pw

# Create your views here.
def UserRegister(request: HttpRequest):
    """ User Register Function
    TODO: redirect after being registered
    """
    Tags = Book_Tag.objects.all()
    if request.method == "POST" and request.POST:
        name = request.POST["name"] # username
        password1 = request.POST["password1"] # password1
        password2 = request.POST["password2"] # password2
        nickname = request.POST["nickname"] # nickname
        gender = request.POST["gender"] # sex
        major = request.POST["major"] # major
        type = request.POST.getlist("type")
        err_msg = "成功注册！请跳转至/login/登录页面进行登录"

        if password1 != password2: # check password
            err_msg = "两次输入的密码不一致！"
            return render(request, "register.html", locals())

        # check password validation
        err_msg_pw = check_password(password1)
        if len(err_msg_pw):
            err_msg = "注册失败！请查看下方错误信息！"
            return render(request, 'register.html', locals())
        
        try:
            # create basic user
            user = User.objects.create_user(username=name, password=password1) 
        except IntegrityError: # If exists
            err_msg = "该用户名已存在！"
            return render(request, "register.html", locals())
        
        try:
            # create platform user
            platform_user = PlatformUser.objects.create(    
                    uid=user,
                    nickname=nickname,
                    gender=list(filter((lambda x: x[1]==gender), PlatformUser.Gender.choices))[0][0],
                    major=list(filter((lambda x: x[1]==major), PlatformUser.Major.choices))[0][0],
                ) 
        except IntegrityError: # If exists
            user.delete()
            err_msg = "该昵称已存在！"
            return render(request, "register.html", locals())
        for tag in type:
            platform_user.type_preference.add(Book_Tag.objects.get(book_tag=tag))
        
        platform_user.save()
        
        return render(request, "register.html", locals())

    else:
        return render(request, "register.html", locals())

def UserLogin(request: HttpRequest):
    """ User Login Function

    Edit: add "auth.login(request, user)"
    """
    if request.method == "POST" and request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password) # Get user by username and password
        if user:
            auth.login(request, user)
            return redirect("/account/%s/" % user.get_username()) # Redirect to the user's page
        else:
            err_msg = "用户名或密码错误！"
            return render(request, "login.html", locals())
    else:
        return render(request, "login.html", locals())

def UserLogout(request: HttpRequest):
    """ User Logout Function
    Modify the login status and redirect to the login page.
    """
    auth.logout(request)
    return HttpResponseRedirect("/account/login/")

@login_required(redirect_field_name="login")
def UserPage(request: HttpRequest, username: str):
    """ User info Page Function
    Any User can visit if log in.
    """
    user = User.objects.get(username=username)
    platform_user = PlatformUser.objects.get(uid=user)

    if request.user.username != username:
        return HttpResponseRedirect("/account/login/")

    return render(request, "user_page.html", locals())
    
def Change_Password(request: HttpRequest):
    """Change Password Function
    """
    platform_user = PlatformUser.objects.get(uid=request.user)
    if request.method == 'POST' and request.POST:
        username = request.POST['username']
        original_password = request.POST['originalpw']
        new_password1 = request.POST['newpw1']
        new_password2 = request.POST['newpw2']
        user = auth.authenticate(username=username, password=original_password)
        err_msg = "密码修改成功！"
        if user:
            if new_password1 != new_password2:
                err_msg = "前后两次输入的密码不一致！"
                return render(request, 'changepw.html', locals())
            err_msg_pw = check_password(new_password1)
            if len(err_msg_pw):
                err_msg = "密码修改失败！请查看下方错误信息！"
                return render(request, 'changepw.html', locals())
            user.set_password(new_password1)
            user.save()
            platfrom_user = PlatformUser.objects.get(uid=user)
            platfrom_user.save()
        else:
            err_msg = "用户名或密码错误！"
        return render(request, 'changepw.html', locals())
    return render(request, 'changepw.html', locals())

@login_required(redirect_field_name='login')
def Edit_Info(request: HttpRequest, username: str):
    Tags = Book_Tag.objects.all()
    platform_user = PlatformUser.objects.get(uid=User.objects.get(username=username))
    if request.user.username != username:
        return HttpResponseRedirect("/account/login/")
    if request.method == "POST" and request.POST:
        nickname = request.POST['nickname']
        gender = request.POST["gender"] 
        major = request.POST["major"] 
        type = request.POST.getlist("type")
        err_msg = "修改成功！"
        try:
            same_nickname = PlatformUser.objects.get(nickname=nickname)
        except PlatformUser.DoesNotExist:
            platform_user.nickname = nickname
            platform_user.gender = list(filter((lambda x: x[1]==gender), PlatformUser.Gender.choices))[0][0]
            platform_user.major=list(filter((lambda x: x[1]==major), PlatformUser.Major.choices))[0][0]
            platform_user.type_preference.clear()
            for tag in type:
                platform_user.type_preference.add(Book_Tag.objects.get(book_tag=tag))
            platform_user.save()
            return render(request, 'edit_info.html', locals())
        if same_nickname:
                err_msg = "修改失败！该昵称已存在！"
                return render(request, 'edit_info.html', locals())
    return render(request, 'edit_info.html', locals())
