import re
import os
import time
from urllib.request import urlopen

# 获取当前执行此程序的目录并且存放起来后续代码需要在此基础上拼接
WORKPATH = os.getcwd()

# 判断是否存在imgs文件夹
if os.path.exists(f"{WORKPATH}/imgs"):
    # 如果有的话则删除该文件夹下的所有文件
    # 其实就是删除上一次获取的图片内容
    for file in os.listdir(WORKPATH+"/imgs"):
        os.remove(WORKPATH+"/imgs/"+file)
else:
    # 如果不存在该文件夹则创建一个imgs文件夹
    os.makedirs(f"{WORKPATH}/imgs/")

# 获取网页全部信息
page_data = urlopen(input("请输入要爬取的贴吧页:"))

# 将读取到的bytes类型转换为str类型
text = str(page_data.read(), "utf-8")

# 提取需要的内容
imgs = re.findall(
    "<img .*? bpic=\"(.*?)\" class=\"threadlist_pic j_m_pic \"", text)

# 显示提示信息
print("\033[31m正在保存照片中...\033[0m")

# 根据获取到的url循环生成图片
for img in imgs:

    # 确定存储的类型(非严谨写法)
    if "jpg" in img:
        img_data = "jpg"
    elif "jpeg" in img:
        img_data = "jpeg"
    else:
        img_data = "png"

    # 解析获取到的图片url
    img_url = urlopen(img)

    # 开始生成图片(名字是当前的时间戳)
    with open(f"{WORKPATH}/imgs/{time.time()}.{img_data}", "wb") as w:
        w.write(img_url.read())

    # 显示已经保存了多少张图片的提示信息
    print(
        f"\r\033[31m已保存\033[0m[\033[32m{len(os.listdir(WORKPATH+'/imgs'))}\033[0m]\033[31m张图片\033[0m",
        end="")

# 显示爬取完成的提示信息
print("\n\033[32m爬取完毕!\033[0m")
# 显示图片的保存目录
print(f"\033[32m图片保存目录: \033[0m\"{WORKPATH}\imgs\\\033[0m\"")
