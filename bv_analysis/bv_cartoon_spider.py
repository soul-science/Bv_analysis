import requests
from bs4 import BeautifulSoup as soup

import re
import json
import csv


style_id = [str(i) for i in range(10010, 10049) if i != 10014]
style_id.append("10102")
styles = ["原创", "漫画改", "小说改", "游戏改", "布袋戏", "热血", "穿越", "奇幻", "战斗", "搞笑", "日常", "科幻",
          "萌系", "治愈", "校园", "少儿", "泡面", "恋爱", "少女", "魔法", "冒险", "历史", "架空", "机战", "神魔", "声控", "运动",
          "励志", "音乐", "推理", "社团", "智斗", "催泪", "美食", "偶像", "乙女", "职场", "特摄"]

style_id = style_id[24:]
styles = styles[24:]


class BvSpider(object):
    def __init__(self):
        self.url = ["https://api.bilibili.com/pgc/season/index/result?"
                    "season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&"
                    "season_month=-1&year=-1&style_id={style_id}&order=3&st=1&sort=0&page=1&"
                    "season_type=1&pagesize=4000&type=1",
                    "https://www.bilibili.com/bangumi/media/md{mid}/"
                    ]
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/90.0.4430.72 Safari/537.36"
        }

        self.pattern = "(?<=__INITIAL_STATE__=){.+}(?=;)"

    def get_mid(self, style):
        response = requests.get(self.url[0].format(style_id=style), headers=self.header)

        if response.status_code == 200:
            data = json.loads(response.content)["data"]["list"]

            return [each["media_id"] for each in data]

    def get_data(self, mid, style, number):

        response = requests.get(self.url[1].format(mid=mid), headers=self.header)

        if response.status_code == 200:
            bs = soup(response.content, "html5lib")
            d = json.loads(re.findall(self.pattern, bs.get_text())[0])
            if "rating" not in d["mediaInfo"]:
                print("no score {style}-{mid} <{number}>".format(style=style, mid=mid, number=number + 1))
                return None
            row = [
                d["mediaInfo"]["title"],
                d["mediaInfo"]["rating"]["score"],
                d["mediaInfo"]["stat"]["views"],
                d["mediaInfo"]["stat"]["series_follow"],
                d["mediaInfo"]["stat"]["danmakus"],
                d["mediaInfo"]["rating"]["count"],
                '|'.join([d["mediaInfo"]["styles"][i]["name"] for i in range(len(d["mediaInfo"]["styles"]))])
            ]

            if "payment" in d["mediaInfo"]:
                row.append(1)
            else:
                row.append(0)
            print("finish {style}-{mid} <{number}>".format(style=style, mid=mid, number=number + 1))
            return row

    def save_csv(self, info, style):
        with open(".\\bilibili\\{style}.csv".format(style=style), "w", newline="", encoding="utf-8-sig") as fp:
            csvWriter = csv.writer(fp)
            csvWriter.writerows(info)

    def run(self):
        for i in range(len(style_id)):
            mid = self.get_mid(style_id[i])
            lines = [["番剧名称", "评分", "播放量", "追番人数", "弹幕总数", "评分人数", "类型", "是否为大会员"]]
            for j in range(len(mid)):
                data = self.get_data(mid[j], styles[i], j)
                if data is not None:
                    lines.append(data)
            self.save_csv(lines, styles[i])


if __name__ == '__main__':
    BvSpider().run()
