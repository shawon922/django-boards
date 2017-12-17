from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Board, Topic, Post
from .forms import NewTopicForm


def home(request):
    boards = Board.objects.all()

    context = {
        'boards': boards,
    }

    return render(request, 'boards/home.html', context)

def board_topics(request, pk=None):
    board = get_object_or_404(Board, pk=pk)

    context = {
        'board': board,
    }
    return render(request, 'boards/topics.html', context)

@login_required
def new_topic(request, pk=None):
    board = get_object_or_404(Board, pk=pk)

    form = NewTopicForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # user = User.objects.first()

        topic = form.save(commit=False)
        topic.board = board
        topic.starter = request.user
        topic.save()

        message = form.cleaned_data.get('message')

        post = Post.objects.create(message=message, topic=topic, created_by=request.user)

        return redirect('boards:board_topics', pk=board.pk)

    context = {
        'board': board,
        'form': form,
    }
    return render(request, 'boards/new_topic.html', context)
