from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .tasks import crawl_bookstore


@csrf_exempt
def tasks(request):
    if request.method == 'GET':
        return _post_tasks()
    else:
        return JsonResponse({"error": "Wrong HTTP method."}, status=405)

def _post_tasks():
    crawl_bookstore()
    return JsonResponse({"message": "Scrapping started."}, status=302)