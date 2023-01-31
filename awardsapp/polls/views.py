from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Estas en la página principal de los Juan Awards")


def detail(request, question_id):
    return HttpResponse(f'Estas viendo la pregunta N°{question_id}')


def results(request, question_id):
    return HttpResponse(f'Estas viendo los resultados de la pregunta N°{question_id}')


def vote(request, question_id):
    return HttpResponse(f'Estas votando la pregunta N°{question_id}')