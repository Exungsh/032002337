import requests
from bs4 import BeautifulSoup
import json
import time

# 统计中国大陆每日本土新增确诊人数及新增无症状感染人数，境外输入类型和疑似病例等无需统计。
# 统计所有省份包括港澳台每日本土新增确诊人数及新增无症状感染人数，境外输入类型和疑似病例等无需统计。
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33'}


def get(target_url):
    area = requests.get(target_url, headers=headers).text  # 爬取网页文字
    bs = BeautifulSoup(area, "html.parser")
    d = bs.findAll('p')  # data存储所有p标签中的内容
    return d


with open("url_list.json") as f:
    url_dict = json.loads(f.read())  # 导入程序get_url产生的json文件
date_list = url_dict.keys()
for date in date_list:
    try_count = 1
    list_len = 0
    p_data = []
    url = url_dict[date]
    while list_len == 0:
        print(date+'第' + str(try_count) + '次尝试')
        try_count += 1
        time.sleep(3)
        p_data = get(url)
        list_len = len(p_data)
    data = ''
    for p in p_data:
        data = data + p.text
    fh = open(date+'.txt', 'w', encoding='utf-8')
    fh.write(data)
    fh.close()
