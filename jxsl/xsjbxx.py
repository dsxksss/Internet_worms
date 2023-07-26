import requests
import json
import csv
import asyncio
import os
from fake_useragent import UserAgent


# 获取当前执行此程序的目录并且存放起来后续代码需要在此基础上拼接
WORKPATH = os.getcwd()
CSVPATH = f"{WORKPATH}/江西水利学生信息.csv"


# 判断是否存在csv文件
if not os.path.exists(CSVPATH):
    with open(CSVPATH, "w", newline="", encoding="utf-8") as w:
        writer = csv.DictWriter(w, fieldnames=["创建时间", "所在班级", "学号", "姓名", "所在系"])
        writer.writeheader()

url = "http://portal.jxslsd.com:4106/api/upp/contentDisplay/queryAppointCard/abd7305a3a1347e596c4f761b41f4e57"


print("请输入你要爬取的学号区间")
start = int(input("开始学号:"))
end = int(input("结束学号:"))


async def getUserData(loginuserid):
    headers = {
        "Loginuserid": loginuserid,
        "User-Agent": UserAgent().random,
        "Accept": "*/*",
        "Host": "portal.jxslsd.com:4106",
        "Connection": "keep-alive",
    }

    response = requests.request("GET", url, headers=headers, data=b"")
    result = json.loads(response.text)
    data = json.loads(result["data"]["data"])
    return data[0]


async def main():
    data_couter = 0
    userids = [str(i) for i in range(start, end + 1)]

    for userid in userids:
        try:
            pure_user = await getUserData(userid)
            user = {
                "创建时间": pure_user["CJSJ"],
                "所在班级": pure_user["BJ"],
                "学号": pure_user["YHBH"],
                "姓名": pure_user["YHMC"],
                "所在系": pure_user["ZY"],
            }
            # 解码并保存学生数据
            with open(CSVPATH, "a", newline="", encoding="utf-8") as w:
                writer = csv.DictWriter(
                    w, fieldnames=["创建时间", "所在班级", "学号", "姓名", "所在系"]
                )
                writer.writerow(user)

            # 显示已经保存了多少个用户的提示信息
            data_couter += 1
            print(
                f"\r\033[31m已保存\033[0m[\033[32m{data_couter}\033[0m]\033[31m个用户\033[0m",
                end="",
            )

        except:
            continue

    print("\n\033[32m获取完毕!\033[0m")


# 运行异步函数
asyncio.run(main())
