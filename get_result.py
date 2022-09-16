import requests
import xlwt
from bs4 import BeautifulSoup
import jieba
import json
from pyecharts.charts import Bar, Grid
from pyecharts.charts import Map
import pyecharts.options as opts
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
    url_dict = json.loads(f.read())# 导入程序get_url产生的json文件
print('可查询从'+list(url_dict.keys())[-1]+'到'+list(url_dict.keys())[0]+'疫情数据')
input_date = input("请输入日期（x月x日）:")
url = url_dict[input_date]
try_count = 1
list_len = 0
data = []
while list_len == 0:
    print('第' + str(try_count) + '次尝试')
    try_count += 1
    time.sleep(5)
    data = get(url)
    list_len = len(data)
# 创建表格
book = xlwt.Workbook()
sheet = book.add_sheet('sheet1')

# ==========新增确诊==========
# 切词
new_prov = []
new_num = []
new_data = data[0].text
cut = jieba.cut(new_data, cut_all=False)  # jieba切词
result = ' '.join(cut)
result = result.split()
date = result[0] + result[1] + result[2] + result[3]  # 当前日期
print(date)

# 整理数据到列表、excel
count = 0
newconfirm = 0
title = ['省份', '新增确诊']
col = 0
for i in title:
    sheet.write(0, col, i)
    col += 1
new_row = 1
for word in result:
    if newconfirm == 1:
        if word.isdigit():
            # print(result[count - 1] + word + '例')
            new_prov.append(result[count - 1])
            new_num.append(int(word))
            sheet.write(new_row, 0, result[count - 1])
            sheet.write(new_row, 1, word)
            new_row += 1
        elif word == '含':
            newconfirm = 0
    elif word.isdigit() and result[count - 2] == '本土':
        newconfirm = 1
        new_sum = word
        print("本土新增确诊:" + word + '例')
    count += 1
new_row += 1
sheet.write(new_row, 0, '总计')
sheet.write(new_row, 1, new_sum)
new_row += 1

# ==========新增无症状==========
wzz_prov = []
wzz_num = []
wzz_data = data[4].text
cut = jieba.cut(wzz_data, cut_all=False)
result = ' '.join(cut)
result = result.split()
count = 0
newwzz = 0
title = ['省份', '新增无症状']
col = 3
for i in title:
    sheet.write(0, col, i)
    col += 1
wzz_row = 1
for word in result:
    if newwzz == 1:
        if word.isdigit():
            # print(result[count - 1] + word + '例')
            wzz_prov.append(result[count - 1])
            wzz_num.append(int(word))
            sheet.write(wzz_row, 3, result[count - 1])
            sheet.write(wzz_row, 4, word)
            wzz_row += 1
    elif word.isdigit() and result[count - 1] == '本土':
        newwzz = 1
        wzz_sum = word
        print("本土新增无症状:" + word + '例')
    count += 1
wzz_row += 1
sheet.write(wzz_row, 3, '总计')
sheet.write(wzz_row, 4, wzz_sum)
wzz_row += 1
book.save(date + '全国新增确诊和无症状人数汇总.xls')

# pyecharts可视化

# 柱状图
# bar_new = (
#     Bar()
#     .add_xaxis(new_prov)
#     .add_yaxis("新增确诊人数", new_num)
#     .set_global_opts(title_opts=opts.TitleOpts(
#         title=date + "全国新增确诊和无症状人数汇总",
#         subtitle='全国共新增确诊' + new_sum + '人，新增无症状' + wzz_sum + "人"),
#         legend_opts=opts.LegendOpts(pos_top="8%")
#     )
# )
# bar_wzz = (
#     Bar()
#     .add_xaxis(wzz_prov)
#     .add_yaxis("新增无症状人数", wzz_num)
#     .set_global_opts(legend_opts=opts.LegendOpts(pos_bottom="40%"))
# )
# (Grid(init_opts=opts.InitOpts(width='1500px', height='600px'))
#  .add(bar_new, grid_opts=opts.GridOpts(pos_top="90px", pos_bottom="60%", height="200px"))
#  .add(bar_wzz, grid_opts=opts.GridOpts(pos_top="60%", height="200px"))
#  ).render(date + '全国新增确诊和无症状人数柱状图.html')
#
# # 地图
# x = []  # 把各省感染人数与各省对应
# for z in zip(list(new_prov), list(new_num)):
#     list(z)
#     x.append(z)
# area_map = Map()
# area_map.add("中国疫情新增确诊分布图", x, "china", is_map_symbol_show=False)
# area_map.set_global_opts(title_opts=opts.TitleOpts(title="中国疫情新增确诊人数分布地图", subtitle=date),
#                          visualmap_opts=opts.VisualMapOpts(
#                              is_piecewise=True,
#                              pieces=[
#                                  {"min": 1500, "label": '>10000人', "color": "black"},
#                                  {"min": 500, "max": 15000, "label": '500-1000人', "color": "#6F171F"},
#                                  {"min": 100, "max": 499, "label": '100-499人', "color": "#C92C34"},
#                                  {"min": 10, "max": 99, "label": '10-99人', "color": "#E35B52"},
#                                  {"min": 1, "max": 9, "label": '1-9人', "color": "#F39E86"}]))
# area_map.render(date + '全国新增确诊地图.html')
