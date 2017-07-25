from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello world,You are at the polls index.")

def detail(request,question_id):
    return HttpResponse("You looking at a question %s" % question_id)

def results(request,question_id):
    response = "You're looking at a result of question %s"
    return HttpResponse(response % question_id)

def vote(request,question_id):
    return HttpResponse("You're vote on question %s ." % question_id)