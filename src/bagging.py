import numpy as np
from random import randrange
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def bs_sampling(x_train, y_train):
    set_size = x_train.shape[0]
    idx_list = []
    y_bs_train = []
    for _ in range(set_size):
        idx = randrange(set_size)
        idx_list.append(idx)
        y_bs_train.append(y_train[idx])
    return x_train[idx_list, :], y_bs_train

def bagging(x_train, y_train, x_test, classifier="NB", rounds=11):
    # x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.1)
    y_test = np.zeros(x_test.shape[0], dtype=int)
    # y_val_pred = np.zeros(x_val.shape[0])
    for i in range(rounds):
        print("\r Round: %d/%d" %(i+1, rounds), end="")
        # create bootstrap sample set
        x_bs_train, y_bs_train = bs_sampling(x_train, y_train)
        if classifier == "NB":
            clf = MultinomialNB()
        elif classifier == "SVM":
            lclf = LinearSVC()
            clf = CalibratedClassifierCV(lclf, method='sigmoid', cv=3)
        elif classifier == "DTREE":
            clf = DecisionTreeClassifier(min_samples_leaf = 5)
        clf.fit(x_bs_train, y_bs_train)
        clf_predict = clf.predict_proba(x_test)[:,1]
        y_test = y_test + np.array(clf_predict)
        # y_val_pred = y_val_pred + np.array(clf.predict_proba(x_val)[:,1])
    # print("Auc score in val set: ", roc_auc_score(y_val, y_val_pred))
    y_test = y_test.tolist()
    y_test = list(map(lambda x: x/rounds, y_test))
    return y_test