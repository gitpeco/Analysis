from io import StringIO
import json
import time
from pprint import pprint
from DrissionPage import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
import csv
from urllib.parse import quote
from io import StringIO
import json
import time
from pprint import pprint
from urllib.parse import quote
from DrissionPage import ChromiumOptions, ChromiumPage

def run_crawler(query):
    # 创建文件对象
    f = open('data.csv', mode='w', encoding='utf-8', newline='')
    # 字典写入方法
    csv_buffer = StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=[
        '职位',
        '城市',
        '区域',
        '街道',
        '公司',
        '薪资',
        '经验',
        '学历',
        '领域',
        '融资',
        '规模',
        '技能要求',
        '基本福利',
    ])
    # 写入表头
    csv_writer.writeheader()

    path = r'D:\BaiduNetdiskDownload\101.0.4951.54_chrome64_stable_windows_installer\chrome\Chrome-bin\chrome.exe'
    ChromiumOptions().set_browser_path(path).save()
    # 实例化浏览器对象
    dp = ChromiumPage()
    # 监听数据包
    dp.listen.start('wapi/zpgeek/search/joblist.json')
    # 访问网站

    url = f'https://www.zhipin.com/web/geek/job?query={query}&city=100010000&page=1'
    dp.get(url)
    # 等待数据包的加载
    resp = dp.listen.wait()

    all_jobs = []  # 用于存储所有页的数据

    # 循环翻页
    for page in range(1, 11):
        print(f'正在采集{page}页的数据内容')

        # 下滑页面到底部
        dp.scroll.to_bottom()
        # 获取响应数据
        json_data = resp.response.body

        """解析数据"""
        # 确保 json_data 是一个字典
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        # 提取职位信息所在列表
        if 'zpData' in json_data and 'jobList' in json_data['zpData']:
            jobList = json_data['zpData']['jobList']
            # for 循环遍历，提取列表里面元素（30个岗位信息）
            for index in jobList:
                # pprint(index)
                dit = {
                    '职位': index.get('jobName', ''),
                    '城市': index.get('cityName', ''),
                    '区域': index.get('areaDistrict', ''),
                    '街道': index.get('businessDistrict', ''),
                    '公司': index.get('brandName', ''),
                    '薪资': index.get('salaryDesc', ''),
                    '经验': index.get('jobExperience', ''),
                    '学历': index.get('jobDegree', ''),
                    '领域': index.get('brandIndustry', ''),
                    '融资': index.get('brandStageName', ''),
                    '规模': index.get('brandScaleName', ''),
                    '技能要求': index.get('skills', ''),
                    '基本福利': index.get('welfareList', ''),
                }
                # 写入数据
                csv_writer.writerow(dit)
                # 将当前岗位信息添加到 all_jobs 列表


        # 点击下一页
        time.sleep(2)
        dp.ele('css:.ui-icon-arrow-right').click()

    dp.close()
    return csv_buffer.getvalue()