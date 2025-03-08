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
from io import StringIO
import csv
@login_required
def search(request):
    results = []
    city_counts = {}  # 用于存储每个城市的招聘数量
    education_counts = {}  # 用于存储每个学历层次的招聘数量
    salary_counts = {}  # 用于存储每个薪资区间的招聘数量

    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        if search_query:
            csv_data = run_crawler(search_query)

            # 解析CSV数据
            csv_buffer = StringIO(csv_data)
            reader = csv.DictReader(csv_buffer)
            results = list(reader)

            # 统计每个城市的招聘数量
            for result in results:
                city = result.get('城市', '未知城市')
                city_counts[city] = city_counts.get(city, 0) + 1

                # 统计每个学历层次的招聘数量
                education = result.get('学历', '未知学历')
                if not education or education == '无要求':
                    education = '没有需求'
                education_counts[education] = education_counts.get(education, 0) + 1

                # 统计每个薪资区间的招聘数量
                salary = result.get('薪资', '未知薪资')
                salary_counts[salary] = salary_counts.get(salary, 0) + 1

            # 关闭缓冲区
            csv_buffer.close()

    # 将城市数据和数量转换为适合Chart.js的格式
    chart_labels = list(city_counts.keys())
    chart_data = list(city_counts.values())

    # 将学历数据和数量转换为适合Chart.js的格式
    education_labels = list(education_counts.keys())
    education_data = list(education_counts.values())

    # 将薪资数据和数量转换为适合Chart.js的格式
    salary_labels = list(salary_counts.keys())
    salary_data = list(salary_counts.values())

    return render(request, 'main/search.html', {
        'results': results,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'education_labels': education_labels,
        'education_data': education_data,
        'salary_labels': salary_labels,
        'salary_data': salary_data
    })

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