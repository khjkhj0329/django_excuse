from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Excuse, Board
from .forms import QuestionForm, AnswerForm


def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Excuse.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'excuse/excuse_list.html', context)
    # return HttpResponse("index 화면")


def detail(request, question_id):
    question = get_object_or_404(Excuse, pk=question_id)
    context = {'question': question}
    return render(request, 'excuse/excuse_detail.html', context)

@login_required(login_url='common:login')
def board_create(request, question_id):
    question = get_object_or_404(Excuse, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('excuse:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'excuse/excuse_detail.html', context)


@login_required(login_url='common:login')
def excuse_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('excuse:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'excuse/excuse_form.html', context)


@login_required(login_url='common:login')
def excuse_modify(request, question_id):
    question = get_object_or_404(Excuse, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('excuse:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('excuse:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'excuse/excuse_form.html', context)


@login_required(login_url='common:login')
def excuse_delete(request, question_id):
    question = get_object_or_404(Excuse, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('excuse:detail', question_id=question.id)
    question.delete()
    return redirect('excuse:index')


@login_required(login_url='common:login')
def board_modify(request, answer_id):
    answer = get_object_or_404(Board, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('excuse:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('excuse:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'excuse/answer_form.html', context)

@login_required(login_url='common:login')
def board_delete(request, answer_id):
    answer = get_object_or_404(Board, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('excuse:detail', question_id=answer.question.id)
