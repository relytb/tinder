import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def save(request):
    # dict_keys(['name', 'like', 'age', 'pics', 'bio'])
    received_json_data = json.loads(request.body.decode("utf-8")) 
    print(received_json_data.keys())
    return HttpResponse("test")
