from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime

from .models import Book, SearchRecord, Tags
from Account.models import PlatformUser

from .RecModel.Recommender import RecSystem


@login_required(redirect_field_name="login")
def index(request):
    platform_user = PlatformUser.objects.get(uid=request.user)
    topk = 3  # How many books to be recommended

    rec = RecSystem()
    book_list = rec.recommend(platform_user, topk=topk)

    books = Book.objects.filter(pk__in=book_list)
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
        pass

    return render(request, "Recommendation/search.html", locals())


@login_required(redirect_field_name="login")
def detailBook(request, book_id):
    platform_user = PlatformUser.objects.get(uid=request.user)
    book = Book.objects.get(id=book_id)
    #booktag = Tags[book.book_tag]
    return render(request, "Recommendation/detailBook.html", locals())


"""
@login_required(redirect_field_name='login')
def detailTopic(request, book_id):
    platform_user = PlatformUser.objects.get(uid=request.user)
    
    return render(request, 'Recommendation/detailTopic.html', locals())
"""
