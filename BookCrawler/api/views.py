from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .tasks import demo_task


@csrf_exempt
def tasks(request):
    if request.method == 'POST':
        return _post_tasks(request)
    else:
        return JsonResponse({}, status=405)

def _post_tasks(request):
    message = request.POST['message']
    print('calling demo_task. message={0}'.format(message))
    demo_task(message)
    return JsonResponse({}, status=302)