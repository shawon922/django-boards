from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import UpdateView 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import SignUpForm


def signup(request):
    ''' 
    ' SignUpForm imported in top
    '''
    form = SignUpForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        ''' 
        ' login is used to authenticate users
        '''
        login(request, user)
        return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'accounts/my_account.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
