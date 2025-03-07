from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User
import subprocess
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .crawler import run_crawler

@login_required
def search(request,query):
    results = []
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        if search_query:
            results = run_crawler(search_query)
    return render(request, 'main/search.html', {'results': results})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('/delete_user')
            else:
                return redirect('/search')
        else:
            return render(request, 'main/login.html', {'error': 'Invalid username or password'})
    return render(request, 'main/login.html')



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('/login/')
        else:
            return render(request, 'main/register.html', {'error': 'Username already exists'})
    return render(request, 'main/register.html')



def delete_user(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            user_id = request.POST['user_to_delete']
            user = User.objects.get(id=user_id)
            user.delete()
            return redirect('/delete_user/')
        users = User.objects.all()
        return render(request, 'admin/delete_user.html', {'users': users})
    else:
        return redirect('/普通用户界面地址')