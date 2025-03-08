from io import StringIO
import csv
# crawler.py
import json
import time
from pprint import pprint
from DrissionPage import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
import csv
from urllib.parse import quote

def run_crawler(query):
    # 创建一个内存中的CSV文件对象
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
    csv_writer.writeheader()

    # 其他爬虫逻辑...

    # 返回CSV数据


    path = r'D:\BaiduNetdiskDownload\101.0.4951.54_chrome64_stable_windows_installer\chrome\Chrome-bin\chrome.exe'
    ChromiumOptions().set_browser_path(path).save()
    dp = ChromiumPage()
    dp.listen.start('wapi/zpgeek/search/joblist.json')

    url = f'https://www.zhipin.com/web/geek/job?query={quote(query)}&city=100010000'
    dp.get(url)
    resp = dp.listen.wait()

    jobList = []
    for page in range(1, 11):
        print(f'正在采集{page}页的数据内容')
        dp.scroll.to_bottom()
        json_data = resp.response.body

        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        if 'zpData' in json_data and 'jobList' in json_data['zpData']:
            jobList = json_data['zpData']['jobList']
            for index in jobList:
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
                csv_writer.writerow(dit)
                pprint(dit)
        else:
            print("未找到 jobList 数据")
        time.sleep(2)
        dp.ele('css:.ui-icon-arrow-right').click()

    dp.close()
    return csv_buffer.getvalue()