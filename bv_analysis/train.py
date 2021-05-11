import pydotplus
from sklearn.model_selection import train_test_split, GridSearchCV  # 数据集划分，超网格搜索+交叉验证
from sklearn.preprocessing import StandardScaler  # 标准化
from sklearn.tree import DecisionTreeClassifier  # 决策树
from sklearn.tree import export_graphviz
import numpy as np

styles = ["原创", "漫画改", "小说改", "游戏改", "布袋戏", "热血", "穿越", "奇幻", "战斗", "搞笑", "日常", "科幻",
          "萌系", "治愈", "校园", "少儿", "泡面", "恋爱", "少女", "魔法", "冒险", "历史", "架空", "机战", "神魔", "声控", "运动",
          "励志", "音乐", "推理", "社团", "智斗", "催泪", "美食", "偶像", "乙女", "职场", "特摄"]

header = ["番剧名称", "评分", "播放量", "追番人数", "弹幕总数", "评分人数", "类型", "是否为大会员"]

x_title = header[2:6]
x_title.append(header[-1])
x_title.extend(styles)


def initialize():
    x = None
    y = None

    with open(".\\bilibili\\bv_x.csv", 'r', encoding='utf-8') as f:
        data = np.loadtxt(f, str, delimiter=",", skiprows=1)
        # 取前5行
        x = np.array(data, dtype=np.float)

    with open(".\\bilibili\\bv_y.csv", 'r', encoding='utf-8') as f:
        data = np.loadtxt(f, str, delimiter=",", skiprows=1)
        # 取前5行
        y = np.array(data, dtype=np.float)

    return train_test_split(x, y)


def decision_tree(train_x, train_y, test_x, test_y, draw=False):
    tree = DecisionTreeClassifier()
    tree.fit(train_x, (train_y * 10).astype('int'))
    accuracy = tree.score(test_x, (test_y * 10).astype('int'))
    predicts = tree.predict(test_x)

    if draw is True:
        export_graphviz(tree, out_file='./tree.dot', feature_names=x_title)

        dot_data = export_graphviz(tree, out_file=None,
                                feature_names=x_title,
                                filled=True, rounded=True,
                                special_characters=True)
        graph = pydotplus.graph_from_dot_data(dot_data)
        # 保存图像到pdf文件
        graph.write_pdf("iris.pdf")

    return accuracy, predicts, tree


if __name__ == '__main__':
    train_x, test_x, train_y, test_y = initialize()
    # print(train_x, train_y, test_x, test_y)
    accuracy, predicts, tree = decision_tree(train_x, train_y, test_x, test_y)
    print(accuracy, predicts)
    print(tree.predict([test_x[0]]))
    print(test_y[0])
