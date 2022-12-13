import requests
from lxml import html
from fake_useragent import UserAgent

# 获取网页内容
# 其中的headers内容是用到了
# fake_useragent伪造请求头
page_content = requests.get(
    "https://movie.douban.com/top250", headers={"User-Agent": UserAgent().random}).content

# 将网页内容转换为html格式
page_etree = html.etree.HTML(page_content)

# 提取当前页面电影标题
movie_titles = page_etree.xpath(
    '//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div/a/span[1]/text()')
# 提取当前页面电影评分
movie_scores = page_etree.xpath('//*[@class="rating_num"]/text()')

# 合并爬取到的电影标题和评分
movies = dict(zip(movie_titles, movie_scores))

# 生成爬取后的文件
with open("./豆瓣TOP前25电影评分.txt", "w", encoding="utf-8") as w:
    # 循环遍历合并后的字典
    for movie_title, movie_score in movies.items():
        # 格式化写入
        w.write(f"[{movie_title}] 评分: {movie_score}\n")

# 结束提示信息
print("---------------\033[32m爬取完成\033[0m---------------")
