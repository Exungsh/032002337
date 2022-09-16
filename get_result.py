import jieba
import re
import xlwt
from pyecharts.charts import Bar, Grid
from pyecharts.charts import Map
import pyecharts.options as opts
input_date = input()
with open('./text_result/'+input_date+'.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    f.close()
print(text)
book = xlwt.Workbook()
sheet = book.add_sheet('sheet1')
new_prov = []
new_num = []
wzz_prov = []
wzz_num = []

# 新增确诊
new_text = re.findall('本土病例.*?）', text)[0]
print(new_text)
cut = jieba.cut(new_text, cut_all=False)  # jieba切词
new_result = ' '.join(cut)
new_result = new_result.split()
print(new_result)
count = 0
title = ['省份', '新增确诊']
col = 0
for i in title:
    sheet.write(0, col, i)
    col += 1
new_row = 1
for word in new_result:
    if word.isdigit():
        if new_result[count - 2] == '本土':
            new_sum = int(word)
        else:
            new_num.append(int(word))
            new_prov.append(new_result[count - 1])
            sheet.write(new_row, 0, new_result[count - 1])
            sheet.write(new_row, 1, int(word))
            new_row += 1
    count += 1
print(new_prov)
print(new_num)


# 新增无症状
wzz_text = re.findall('新增无症状感染者.*?）', text)[0]
print(wzz_text)
cut = jieba.cut(wzz_text, cut_all=False)  # jieba切词
wzz_result = ' '.join(cut)
wzz_result = wzz_result.split()
count = 0
wzz_flag = 0
title = ['省份', '新增无症状']
col = 3
for i in title:
    sheet.write(0, col, i)
    col += 1
wzz_row = 1

for word in wzz_result:
    if word.isdigit():
        if wzz_result[count - 1] == '本土':
            wzz_sum = int(word)
            wzz_flag = 1
        elif wzz_flag == 1 and word.isdigit():
            wzz_num.append(int(word))
            wzz_prov.append(wzz_result[count - 1])
            sheet.write(wzz_row, 3, wzz_result[count - 1])
            sheet.write(wzz_row, 4, int(word))
            wzz_row += 1
    count += 1
print(wzz_prov)
print(wzz_num)
book.save('全国新增确诊和无症状人数汇总.xls')


bar_new = (
    Bar()
    .add_xaxis(new_prov)
    .add_yaxis("新增确诊人数", new_num)
    .set_global_opts(title_opts=opts.TitleOpts(
        title=input_date+"全国新增确诊和无症状人数汇总",
        subtitle='全国共新增确诊' +str(new_sum)+ "人，新增无症状"+str(wzz_sum)+'人'),
        legend_opts=opts.LegendOpts(pos_top="8%")
    )
)
bar_wzz = (
    Bar()
    .add_xaxis(wzz_prov)
    .add_yaxis("新增无症状人数", wzz_num)
    .set_global_opts(legend_opts=opts.LegendOpts(pos_bottom="40%"))
)
(Grid(init_opts=opts.InitOpts(width='1500px', height='600px'))
 .add(bar_new, grid_opts=opts.GridOpts(pos_top="90px", pos_bottom="60%", height="200px"))
 .add(bar_wzz, grid_opts=opts.GridOpts(pos_top="60%", height="200px"))
 ).render(input_date+'全国新增确诊和无症状人数柱状图.html')
# 地图
x = []  # 把各省感染人数与各省对应
for z in zip(list(new_prov), list(new_num)):
    list(z)
    x.append(z)
area_map = Map()
area_map.add("中国疫情新增确诊分布图", x, "china", is_map_symbol_show=False)
area_map.set_global_opts(title_opts=opts.TitleOpts(title="中国疫情新增确诊人数分布地图", subtitle=input_date),
                         visualmap_opts=opts.VisualMapOpts(
                             is_piecewise=True,
                             pieces=[
                                 {"min": 1500, "label": '>10000人', "color": "black"},
                                 {"min": 500, "max": 15000, "label": '500-1000人', "color": "#6F171F"},
                                 {"min": 100, "max": 499, "label": '100-499人', "color": "#C92C34"},
                                 {"min": 10, "max": 99, "label": '10-99人', "color": "#E35B52"},
                                 {"min": 1, "max": 9, "label": '1-9人', "color": "#F39E86"}]))
area_map.render(input_date + '全国新增确诊地图.html')

import cProfile
import re
cProfile.run('re.compile("foo|bar")')