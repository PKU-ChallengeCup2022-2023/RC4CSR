from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from .models import PlatformUser
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from Recommendation.models import Book_Tag

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
        print(request.POST)
        err_msg = "成功注册！请跳转至/login/登录页面进行登录"

        if password1 != password2: # check password
            err_msg = "两次输入的密码不一致！"
            return render(request, "register.html", locals())

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
            print(tag)
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
    if request.method == "POST" and request.POST:
        return UserLogout(request)
    return render(request, "user_page.html", locals())
    

