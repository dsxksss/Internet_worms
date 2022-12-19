import csv
import requests
from lxml import html
from fake_useragent import UserAgent

movies = []
movie_page_urls = []
movie_titles = []
movie_actors = []
movie_dates = []
movie_scores = []

page_content = requests.get("https://movie.douban.com/top250",
                            headers={"User-Agent": UserAgent().random}).content
# 将网页内容转换为html格式
page_etree = html.etree.HTML(page_content)
movie_page_urls += page_etree.xpath(
    '//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div/a/@href')

for url in movie_page_urls:
    now_page_content = requests.get(
        url, headers={"User-Agent": UserAgent().random}).content
    now_page_etree = html.etree.HTML(now_page_content)

    # 获取当前电影名称信息
    movie_titles += (now_page_etree.xpath(
        '//*[@id="content"]/h1/span[1]/text()'))

    # 获取当前电影主演信息
    actor1 = now_page_etree.xpath(
        '//*[@id="info"]/span[3]/span[2]/*[1]/text()')
    actor2 = now_page_etree.xpath(
        '//*[@id="info"]/span[3]/span[2]/*[2]/text()')
    movie_actor = f"{actor1[0]}/{actor2[0]}"
    movie_actors.append(movie_actor)

    # 获取当前电影时间信息
    movie_dates.append(now_page_etree.xpath(
        '//*[@id="content"]/h1/span[2]/text()')[0][1:5])

    # 获取当前电影评分信息
    movie_scores += (now_page_etree.xpath(
        '//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()'))

# 处理成规定的csv写入格式
for i in range(len(movie_page_urls)):
    movies.append(
        {"编号": i+1, "电影名称": movie_titles[i], "演员": movie_actors[i], "时间": movie_dates[i], "评分": movie_scores[i]})


# 生成爬取后的文件
with open("./豆瓣top25电影信息.csv", "w", encoding="utf-8") as w:
    writer = csv.DictWriter(w, fieldnames=["编号", "电影名称", "演员", "时间", "评分"])
    writer.writeheader()  # 写入csv头
    writer.writerows(movies)  # 写入全部电影数据

# 结束提示信息
print("---------------\033[32m爬取完成\033[0m---------------")
