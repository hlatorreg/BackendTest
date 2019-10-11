from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json

from .tasks import crawl_bookstore
from .tasks import get_all_model_categories
from .tasks import get_model_book_by_id
from .tasks import get_model_book_by_upc
from .tasks import create_api_user
from .tasks import is_authenticated

@csrf_exempt
def tasks(request):
    if request.method == 'GET':
        return _post_tasks()
    else:
        return JsonResponse({"error": "Wrong HTTP method."}, status=405)

@csrf_exempt
def get_categories(request):
    auth_flag = is_authenticated(request)
    if request.method == 'POST' and request.content_type == 'application/json' and auth_flag:
        categories = list(get_all_model_categories())
        return JsonResponse(categories, status=200, safe=False)
    elif not auth_flag:
        return JsonResponse({"error": "Wrong user credentials"}, status=401)
    else:
        return JsonResponse({"error": "Wrong HTTP method."}, status=405)

@csrf_exempt
def get_book(request, ide):
    auth_flag = is_authenticated(request)
    if request.method == 'POST' and request.content_type == 'application/json' and 'upc' not in request.path and auth_flag:
        book = get_model_book_by_id(ide)
        return JsonResponse(book, status=200, safe=False)
    elif request.method == 'POST' and request.content_type == 'application/json' and auth_flag:
        book = get_model_book_by_upc(ide)
        return JsonResponse(book, status=200, safe=False)
    elif not auth_flag:
        return JsonResponse({"error": "Wrong user credentials"}, status=401)
    else:
        return JsonResponse({"error": "Bad request structure."}, status=405)

@csrf_exempt
def create_user(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        user_data = json.loads(request.body.decode('utf-8'))
        if 'username' not in user_data.keys() or 'password' not in user_data.keys():
            return JsonResponse({"error": "Wrong JSON structure."}, status=406)
        else:
            result = create_api_user(user_data['username'], user_data['password'])
            return JsonResponse({"result": str(result)}, status=201)

    else:
        return JsonResponse({"error": "Bad request"}, status=401)

def _post_tasks():
    crawl_bookstore()
    return JsonResponse({"message": "Scrapping started."}, status=202)