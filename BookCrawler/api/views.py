from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .tasks import crawl_bookstore
from .tasks import get_all_model_categories
from .tasks import get_model_book_by_id
from .tasks import get_model_book_by_upc


@csrf_exempt
def tasks(request):
    if request.method == 'GET':
        return _post_tasks()
    else:
        return JsonResponse({"error": "Wrong HTTP method."}, status=405)

@csrf_exempt
def get_categories(request):
    if request.method == 'GET':
        categories = list(get_all_model_categories())
        return JsonResponse(categories, status=200, safe=False)
    else:
        return JsonResponse({"error": "Wrong HTTP method."}, status=404)

@csrf_exempt
def get_book(request, ide):
    if request.method == 'GET' and 'upc' not in request.path:
        book = get_model_book_by_id(ide)
        return JsonResponse(book, status=200, safe=False)
    elif request.method == 'GET':
        book = get_model_book_by_upc(ide)
        return JsonResponse(book, status=200, safe=False)
    else:
        return JsonResponse({"error": "Bad request structure."}, status=404)

def _post_tasks():
    crawl_bookstore()
    return JsonResponse({"message": "Scrapping started."}, status=302)