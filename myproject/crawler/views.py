from django.shortcuts import render
from .utils import run_crawler


def crawler_view(request, query):
    # 运行爬虫
    csv_data = run_crawler(query)

    # 打印爬虫返回的数据
    print(csv_data)

    # 将 CSV 数据解析为列表
    data = []
    if csv_data:
        for row in csv_data.split('\n'):
            if row.strip():
                data.append(row.split(','))

    # 渲染结果页面
    return render(request, 'results.html', {'data': data})