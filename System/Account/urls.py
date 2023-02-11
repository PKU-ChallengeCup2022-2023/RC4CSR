from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserRegister, name="register"),
    path("login/", views.UserLogin, name="login"),
    path("changepw/", views.Change_Password, name="chagnepw"),
    path("<slug:username>/", views.UserPage),
    path("<slug:username>/editinfo/", views.Edit_Info, name="editinfo"),
]