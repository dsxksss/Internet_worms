import re
import csv
import requests

url = "https://tieba.baidu.com/f?ie=utf-8&kw=%E6%B1%9F%E8%A5%BF%E6%B0%B4%E5%88%A9%E8%81%8C%E4%B8%9A%E5%AD%A6%E9%99%A2&fr=search"  # 要自动爬取的网页url
url_list = []
for i in range(0, 500, 50):
    print(i)
url_hou = str(i)
print(url_hou)
url_list.append(url+url_hou)
print(url_list)

my_head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52'}

text = requests.get(url, headers=my_head).content.decode()  # 对网页源码进行解码输出
print(text)

list = re.findall(r'class="j_th_tit ">(.*?)</ a>', text)
dict_list = []
for item in list:
    dict_list.append({"贴吧标题": item})
with open("./result.csv", "w", newline="", encoding="utf-8") as w:
    writer = csv.DictWriter(w, fieldnames=["贴吧标题"])
    writer.writeheader()
    writer.writerows(dict_list)
print(dict_list)


print("爬取成功")
