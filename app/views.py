from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from file_utils import _init_folders, save_profile, _get_profile


def save(request):
    """ save endpoint """
    _init_folders()
    save_profile(_get_profile(request))
    return HttpResponse("test")
