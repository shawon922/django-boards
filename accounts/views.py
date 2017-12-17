from django.contrib.auth import login
from django.shortcuts import render, redirect
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
