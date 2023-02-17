from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Estás en la página principal")

def detail(request, question_id):
    return HttpResponse(f"Estás viendo la pregunta ID {question_id}")


def results(request, question_id):
    return HttpResponse(f"Estás viendo los resultados de la pregunta ID {question_id}")


def vote(request, question_id):
    return HttpResponse(f"Estás votando por la pregunta ID {question_id}")