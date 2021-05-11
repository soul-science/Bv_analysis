import csv
from itertools import islice

style_id = [str(i) for i in range(10010, 10049) if i != 10014]
style_id.append("10102")
styles = ["原创", "漫画改", "小说改", "游戏改", "布袋戏", "热血", "穿越", "奇幻", "战斗", "搞笑", "日常", "科幻",
          "萌系", "治愈", "校园", "少儿", "泡面", "恋爱", "少女", "魔法", "冒险", "历史", "架空", "机战", "神魔", "声控", "运动",
          "励志", "音乐", "推理", "社团", "智斗", "催泪", "美食", "偶像", "乙女", "职场", "特摄"]

header = ["番剧名称", "评分", "播放量", "追番人数", "弹幕总数", "评分人数", "类型", "是否为大会员"]

x_title = header[2:6]
x_title.append(header[-1])
x_title.extend(styles)

y_title = [header[1]]


def read_csv(style):
    items = []
    with open(".\\bilibili\\{style}.csv".format(style=style), "r", encoding="utf-8-sig") as fp:
        csvRead = csv.reader(fp)
        for item in islice(csvRead, 1, None):
            items.append(tuple(item))

    return items


def save_csv(info, name):
    with open(".\\bilibili\\{name}.csv".format(name=name), "w", newline="", encoding="utf-8-sig") as fp:
        csvWriter = csv.writer(fp)
        csvWriter.writerows(info)


def convert():
    total = []
    x = []
    y = []
    for style in styles:
        total.extend(read_csv(style))

    total = list(set(total))
    for each in total:
        hot = [0] * len(styles)
        for s in each[6].split("|"):
            try:
                hot[styles.index(s)] = 1
            except Exception:
                continue

        xx = list(each[2:6])
        xx.append(each[-1])
        xx.extend(hot)
        x.append(xx)
        y.append([each[1]])

    total.insert(0, header)
    x.insert(0, x_title)
    y.insert(0, y_title)
    save_csv(total, "全部")
    save_csv(x, "bv_x")
    save_csv(y, "bv_y")


if __name__ == '__main__':
    convert()
