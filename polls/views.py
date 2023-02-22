from django.shortcuts import render, get_object_or_404
from django.utils.html import escape
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question

# Create your views here.
def index(request):
    latest_question_list = Question.objects.all()
    print(latest_question_list)
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list,
    });

def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, "polls/detail.html", {
        "question": question,
    });


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/results.html", {
        'question': question,
    })


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    choice   = request.POST.get('choice')

    try:
        selected_choice = question.choice_set.get(pk=choice)
    except:
        return render(request, "polls/detail.html", {
            'question': question,
            'error_message': "no elegiste una respuesta",
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=({question.id})))