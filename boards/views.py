from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import View, UpdateView, ListView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


''' def home(request):
    boards = Board.objects.all()

    context = {
        'boards': boards,
    }

    return render(request, 'boards/home.html', context)
 '''

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'

''' def board_topics(request, pk=None):
    page_var = 'page'
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated')
    paginator = Paginator(queryset, 20)

    page = request.GET.get(page_var, 1)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    

    context = {
        'board': board,
        'topics': topics,
        'page_var': page_var,
    }
    return render(request, 'boards/topics.html', context) '''


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated')
        return queryset

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

        return redirect('boards:topic_posts', pk=board.pk, topic_pk=topic.pk)

    context = {
        'board': board,
        'form': form,
    }
    return render(request, 'boards/new_topic.html', context)

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    context = {
        'topic': topic,
    }
    return render(request, 'boards/topic_posts.html', context)

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    form = PostForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.topic = topic
        post.created_by = request.user
        post.save()

    context = {
        'topic': topic,
        'form': form,
    }

    return render(request, 'boards/reply_topic.html', context)


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    context_object_name = 'post'
    fields = ['message',]
    pk_url_kwarg = 'post_pk'    
    template_name = 'boards/edit_post.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(create_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.update_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
