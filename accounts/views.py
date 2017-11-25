from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def signup(request):
    ''' 
    ' UserCreationForm imported in top
    '''
    form = UserCreationForm(request.POST or None)

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


def signin(request):
    return render(request, 'accounts/signin.html')


def signout(request):
    pass
