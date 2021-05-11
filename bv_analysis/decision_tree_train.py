from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV  # 数据集划分，超网格搜索+交叉验证
from sklearn.preprocessing import StandardScaler    # 标准化
from sklearn.preprocessing import MinMaxScaler

from sklearn.neighbors import KNeighborsClassifier  # KNN近邻算法
from sklearn.naive_bayes import MultinomialNB   # 朴素贝叶斯算法
from sklearn.tree import DecisionTreeClassifier # 决策树

from sklearn.tree import export_graphviz
import pandas as pd


class IrisTraining:
    def __init__(self):
        self.iris = load_iris()
        self.stdscaler = StandardScaler(with_mean=False)
        # self.stdscaler = MinMaxScaler()
        self.neighbors = GridSearchCV(KNeighborsClassifier(),
                                      param_grid={'n_neighbors': [1, 3, 5, 7, 9]}, cv=10)
        self.bayes = MultinomialNB(alpha=1.0)
        self.decision_tree = DecisionTreeClassifier(criterion='entropy')

        self.train_features,\
        self.test_features,\
        self.train_targets,\
        self.test_targets = train_test_split(self.iris.data, self.iris.target)

        self.train_features = self.stdscaler.fit_transform(self.train_features)
        self.test_features = self.stdscaler.fit_transform(self.test_features)

        self.KNN_predict = None
        self.KNN_accuracy = None

        self.Bayes_predict = None
        self.Bayes_accuracy = None

        self.Decision_tree_predict = None
        self.Decision_tree_accuracy = None

    def run_KNN(self):
        # grid = GridSearchCV(self.neighbors, param_grid=[1, 3, 5, 7, 9], cv=10)
        self.neighbors.fit(self.train_features, self.train_targets)
        self.KNN_accuracy = self.neighbors.score(self.test_features, self.test_targets)
        predicts = self.neighbors.predict(self.test_features)
        self.KNN_predict = pd.DataFrame()
        for i in range(len(self.iris.feature_names)):
            self.KNN_predict[self.iris.feature_names[i]] = self.test_features[:, i]
        self.KNN_predict['original_target'] = self.test_targets
        self.KNN_predict['predict_target'] = predicts
        p = []
        for i in range(len(predicts)):
            if self.test_targets[i] == predicts[i]:
                p.append(True)
            else:
                p.append(False)
        self.KNN_predict['yes?'] = p

    def get_KNN_accuracy(self):
        return self.KNN_accuracy

    def get_KNN_predict(self):
        return self.KNN_predict

    def run_Bayes(self):
        self.bayes.fit(self.train_features, self.train_targets)
        self.Bayes_accuracy = self.bayes.score(self.test_features, self.test_targets)

        predicts = self.bayes.predict(self.test_features)
        self.Bayes_predict = pd.DataFrame()
        for i in range(len(self.iris.feature_names)):
            self.Bayes_predict[self.iris.feature_names[i]] = self.test_features[:, i]
        self.Bayes_predict['original_target'] = self.test_targets
        self.Bayes_predict['predict_target'] = predicts
        p = []
        for i in range(len(predicts)):
            if self.test_targets[i] == predicts[i]:
                p.append(True)
            else:
                p.append(False)
        self.Bayes_predict['yes?'] = p

    def get_Bayes_accuracy(self):
        return self.Bayes_accuracy

    def get_Bayes_predict(self):
        return self.Bayes_predict

    def run_Decision_tree(self):
        # grid = GridSearchCV(self.neighbors, param_grid=[1, 3, 5, 7, 9], cv=10)
        self.decision_tree.fit(self.train_features, self.train_targets)
        self.Decision_tree_accuracy = self.decision_tree.score(self.test_features, self.test_targets)
        predicts = self.decision_tree.predict(self.test_features)
        self.Decision_tree_predict = pd.DataFrame()
        for i in range(len(self.iris.feature_names)):
            self.Decision_tree_predict[self.iris.feature_names[i]] = self.test_features[:, i]
        self.Decision_tree_predict['original_target'] = self.test_targets
        self.Decision_tree_predict['predict_target'] = predicts
        p = []
        for i in range(len(predicts)):
            if self.test_targets[i] == predicts[i]:
                p.append(True)
            else:
                p.append(False)
        self.Decision_tree_predict['yes?'] = p

    def get_Decision_tree_accuracy(self):
        return self.Decision_tree_accuracy

    def get_Decision_tree_predict(self):
        return self.Decision_tree_predict

    def get_Decision_tree_dot(self):
        export_graphviz(self.decision_tree, out_file='./tree.dot', feature_names=self.iris.feature_names)


if __name__ == '__main__':
    iris_train = IrisTraining()
    iris_train.run_KNN()
    iris_train.run_Bayes()
    iris_train.run_Decision_tree()
    iris_train.get_Decision_tree_dot()
    print('KNN近邻算法accuracy：\n', iris_train.get_KNN_accuracy())
    print('Bayes朴素贝叶斯算法accuracy：\n', iris_train.get_Bayes_accuracy())
    print('Decision_Tree决策树算法accuracy：\n', iris_train.get_Decision_tree_accuracy())
    # print(iris_train.get_accuracy())
    # print(iris_train.get_predict())
    # print(iris_train.neighbors.best_params_)
    # print(iris_train.neighbors.best_index_)
    # print(iris_train.neighbors.best_score_)
    # print(iris_train.neighbors.best_estimator_)
    # print(iris_train.neighbors.cv_results_)