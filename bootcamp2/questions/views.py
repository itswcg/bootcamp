from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bootcamp2.decorators import ajax_required

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


def _questions(request, questions, active):
    paginator = Paginator(questions, 10)
    page = request.GET.get('page')

    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    context = {'questions': questions, 'active': active}
    return render(request, 'questions/questions.html', context)


def questions(request):
    return unanswered(request)


def answered(request):
    questions = Question.get_answered()
    return _questions(request, questions, 'answered')


def unanswered(request):
    questions = Question.get_unanswered()
    return _questions(request, questions, 'unanswered')


def all_question(request):
    questions = Question.objects.all()
    return _questions(request, questions, 'all')


@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if not form.is_valid():
            return render(request, 'questions/ask.html', {'form': form})

        question = Question()
        question.user = request.user
        question.title = form.cleaned_data.get('title')
        question.description = form.cleaned_data.get('description')
        question.save()

        tags = form.cleaned_data.get('tags')
        question.create_tags(tags)
        return redirect('/questions/')
    else:
        form = QuestionForm()

    return render(request, 'questions/ask.html', {'form': form})


def question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = AnswerForm(initial={'question': question})
    context = {'question': question, 'form': form}
    return render(request, 'questions/question.html', context)


@login_required
def answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user = request.user
            answer = Answer()
            answer.user = user
            answer.question = form.cleaned_data.get('question')
            answer.description = form.cleaned_data.get('description')
            answer.save()
            # user.profile.notify_answered(answer.question)
            return redirect(f'/questions/{answer.question.pk}/')
        else:
            question = form.cleaned_data.get('question')
            context = {'question': question, 'form': form}
            return render(request, 'questions/question.html', context)
    else:
        return redirect('/questions/')
