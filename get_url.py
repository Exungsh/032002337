from bs4 import BeautifulSoup
import json
import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
    'cookie': 'yfx_c_g_u_id_10006654=_ck22090519332413519823867466701; yfx_mr_f_10006654=::market_type_free_search::::baidu::%e5%8d%ab%e5%81%a5%e5%a7%94::::::www.baidu.com::::pmf_from_free_search; sVoELocvxVW0S=5RosqBPGzMdJfz75I8P67Rd2.hCr5nViXEE6I62vPT82.o0rd0vDV3JOUHIC5cgJOo4KRaQPG_PQf_N4NNSPK2q; insert_cookie=67313298; yfx_f_l_v_t_10006654=f_t_1662377604354__r_t_1662953123120__v_t_1662960189368__r_c_4; _gscu_2059686908=62960380j4mi1g41; _gscbrs_2059686908=1; _gscs_2059686908=62960380j7fc1n41|pv:2; yfx_mr_10006654=::market_type_free_search::::baidu::%e5%8d%ab%e5%81%a5%e5%a7%94::::::www.baidu.com::::pmf_from_free_search; yfx_key_10006654=%e5%8d%ab%e5%81%a5%e5%a7%94; wzws_cid=f76d5c1fbce57a6e50286ad283c6aa319b83a82a166c12976ed97d2bc4c7b27988c1fe5cd65aee248cc8c30c1291e1b9b1ae6cd78753e6b0e6f1afb8d8fa605882c8352be20dcc0f7b699603a81b36f524af3c7c6aac6bd50464f5b314eb03ed; security_session_verify=b64ab9c3eafc52bad90a088197457732; sVoELocvxVW0T=53S4DgCW8SXlqqqDkWk9t1qdWu.ooCbQCUUVGF.y.zq24arD_EJ2evkz5z2KPcWTnm9U9hocL_YlFpwfCDEnVjufCDNWE88F2moo0QAjA2a6LPz0Af8BqgJ.yJn1IPNpLSLYV3AwsTjdj6oPmq6KhruPB0Idj8xyz1HCLeN.L8_utGdHVnRovKRThgmgBdg7_mNPOP0DU9X.A3_dvBfVLVeE4GdsFJgV_kLAHLPdp7mTymI7C1HccAwOaTXicV_c7ZEvUQY5KWMrC1jml.24fAbGTfUSzc2W2Y6e_0RhSFq2dcVhlC3iaVyn5PGxkdLYhYUB72UqP9uW0b9wLY0RNOEZk4hfXFiiOgDboONlXPBPG'
}


def get(target_url):
    date = []
    url = []
    area = requests.get(target_url, headers=headers).text  # 爬取网页文字
    bs = BeautifulSoup(area, "html.parser")
    a_url = bs.select('.list > ul > li > a')  # 选择网址
    span_date = bs.select('.list > ul > li > span')  # 选择日期
    for a in a_url:
        url.append('http://www.nhc.gov.cn/' + a['href'])
    for span in span_date:
        date.append(span.text)
    result = dict(zip(date, url))  # 打包为字典
    return result


url_dict = {}
base_url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd"
for i in range(1, 41):
    if i == 1:
        target_url = base_url + '.shtml'
        print(target_url)
    else:
        target_url = base_url + '_' + str(i) + '.shtml'
        print(target_url)
    list_len = 0
    try_count = 1
    while list_len == 0:
        print('第' + str(i) + '页' + '第' + str(try_count) + '次尝试')
        try_count += 1
        udict = get(target_url)
        list_len = len(udict)
    url_dict.update(udict)

# 将字典存为json文件
with open("url_list.json", "w") as f:
    f.write(json.dumps(url_dict, indent=4))
print("完成！")