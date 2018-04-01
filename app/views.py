import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def save(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))
        print(received_json_data)
    return HttpResponse("test")
