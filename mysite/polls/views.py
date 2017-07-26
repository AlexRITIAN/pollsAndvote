from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.template import loader

from .models import Question,Choice

# Create your views here.
def index(request):
    last_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'last_question_list':last_question_list,
    }
    return render(request,'polls/index.html',context)

def detail(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',
    {'question':question,'error_message':"You didn't select choice"})
    else:
        select_choice.votes += 1
        select_choice.save()
    return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))