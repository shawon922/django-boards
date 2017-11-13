from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Board


def home(request):
    boards = Board.objects.all()

    context = {
        'boards': boards,
    }

    return render(request, 'boards/home.html', context)

def board_topics(request, pk=None):
    board = get_object_or_404(Board, pk=pk)
    
    ''' 
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404 
    '''

    context = {
        'board': board,
    }
    return render(request, 'boards/topics.html', context)
