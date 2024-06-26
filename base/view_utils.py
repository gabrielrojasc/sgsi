import contextlib

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator


def paginate(request, objects, page_size=25):
    paginator = Paginator(objects, page_size)
    page = request.GET.get("p")

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects


def clean_query_string(request):
    clean_query_set = request.GET.copy()

    clean_query_set = {k: v for k, v in request.GET.items() if k != "o"}

    with contextlib.suppress(KeyError):
        del clean_query_set["p"]

    mstring = []
    for key in clean_query_set:
        valuelist = request.GET.getlist(key)
        mstring.extend([f"{key}={val}" for val in valuelist])

    return "&".join(mstring)
