from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime

from .models import Book, SearchRecord
from Account.models import PlatformUser

from .RecModel.Recommender import RecSystem
from .RecModel.preprocess import *


@login_required(redirect_field_name="login")
def index(request):
    platform_user = PlatformUser.objects.get(uid=request.user)
    rec = RecSystem()
    topk = 3  # How many books to be recommended
    book_list = []

    """ Get user's preference tag_id, store in list $preference """
    preference = []
    preference_query = platform_user.type_preference.filter(platformuser=platform_user)
    for item in preference_query:
        preference.append(item.tag_id)
    print(preference)

    """ NN Recommendation """
    nn_input = preprecess_nn(list(preference))
    book_list = rec.recommend(nn_input, topk=topk, flag=0)

    # TODO: Implement VAE model

    """ Note: $book_list has been filled here. """
    # print(book_list)

    return render(request, "Recommendation/index.html", locals())


@login_required(redirect_field_name="login")
def search(request: HttpRequest):
    platform_user = PlatformUser.objects.get(uid=request.user)
    if request.method == "GET" and request.GET:
        book_name = request.GET["name"]
        # TODO: exact fitting now, should be enhanced
        try:
            book_found = Book.objects.get(bookname=book_name)
        except Book.DoesNotExist:
            err_msg = "书目不存在！"
            # TODO: add function: allow user upload books
            return render(request, "Recommendation/search.html", locals())
        record_new = SearchRecord.objects.create(
            searcher=PlatformUser.objects.get(uid=request.user),
            search_tag=book_found.book_tag,
            search_cont=book_name,
            search_time=datetime.datetime.now(),
        )
        err_msg = "搜索成功，以下是该书目详情页面："
    else:
        err_msg = "搜索失败"

    return render(request, "Recommendation/search.html", locals())


@login_required(redirect_field_name="login")
def detailBook(request, book_id):
    platform_user = PlatformUser.objects.get(uid=request.user)
    book = Book.objects.get(id=book_id)
    return render(request, "Recommendation/detailBook.html", locals())


"""
@login_required(redirect_field_name='login')
def detailTopic(request, book_id):
    platform_user = PlatformUser.objects.get(uid=request.user)
    
    return render(request, 'Recommendation/detailTopic.html', locals())
"""
