import csv
import time
import requests
from lxml import html
from fake_useragent import UserAgent
from multiprocessing.dummy import Pool


def get_urls():
    page_content = requests.get(
        "https://movie.douban.com/top250", headers={"User-Agent": UserAgent().random}).content
    # 将网页内容转换为html格式
    page_etree = html.etree.HTML(page_content)
    movie_page_urls = page_etree.xpath(
        '//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div/a/@href')
    return movie_page_urls


def get_html_content(url):
    now_page_content = requests.get(
        url, headers={"User-Agent": UserAgent().random}).content
    return now_page_content


def get_movie_info(html_content):
    now_page_etree = html.etree.HTML(html_content)

    # 获取当前电影排名
    movie_top_num = now_page_etree.xpath(
        '//*[@id = "content"]/div[1]/span[1]/text()')[0][3:]

    # 获取当前电影名称信息
    movie_title = (now_page_etree.xpath(
        '//*[@id="content"]/h1/span[1]/text()'))[0]

    # 获取当前电影主演信息
    actor1 = now_page_etree.xpath(
        '//*[@id="info"]/span[3]/span[2]/*[1]/text()')
    actor2 = now_page_etree.xpath(
        '//*[@id="info"]/span[3]/span[2]/*[2]/text()')
    movie_actor = f"{actor1[0]}/{actor2[0]}"

    # 获取当前电影时间信息
    movie_date = now_page_etree.xpath(
        '//*[@id="content"]/h1/span[2]/text()')[0][1:5]

    # 获取当前电影评分信息
    movie_score = (now_page_etree.xpath(
        '//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()'))[0]

    # 处理成规定的csv写入格式
    movie = {"编号": movie_top_num, "电影名称": movie_title,
             "演员": movie_actor, "时间": movie_date, "评分": movie_score}
    return movie


def save_file(data):
    # 生成爬取后的文件
    with open("./豆瓣top25电影信息.csv", "a+", encoding="utf-8", newline="") as w:
        writer = csv.DictWriter(w, fieldnames=["编号", "电影名称", "演员", "时间", "评分"])
        writer.writerow(data)


def main(url):
    html_content = get_html_content(url)
    data = get_movie_info(html_content)
    save_file(data)


# 结束提示信息
if __name__ == "__main__":
    start_time = time.time()  # 记录程序开始运行时间
    # 生成爬取后的文件
    w = open("./豆瓣top25电影信息.csv", "w", encoding="utf-8", newline="")
    writer = csv.DictWriter(w, fieldnames=["编号", "电影名称", "演员", "时间", "评分"])
    writer.writeheader()
    w.close()

    urls = get_urls()
    pool = Pool(2)
    pool.map(main, urls)
    end_time = time.time()  # 记录程序结束运行时间
    print('运行耗时 %f second' % (end_time - start_time))

    print("---------------\033[32m爬取完成\033[0m---------------")
