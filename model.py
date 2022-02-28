from functools import reduce
from operator import mul

import joblib
import pandas
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier

from encoder import encodes


def get_data():
    combat_logs = pandas.read_csv("combat_log.csv")
    target = combat_logs['Winner']
    features = combat_logs.drop(columns=['Winner'])
    features["Attacker"] = features["Attacker"].apply(encodes)
    features["Defender"] = features["Defender"].apply(encodes)
    return features, target


def find_best_fit():
    features, target = get_data()
    param_dist = {
        "criterion": ["gini", "entropy"],
        "max_depth": [9, 10, 11, 12],
    }
    model = RandomizedSearchCV(
        RandomForestClassifier(
            n_estimators=299,
            random_state=42,
            n_jobs=1,
        ),
        cv=3,
        n_jobs=8,
        n_iter=reduce(mul, map(len, param_dist.values())),
        param_distributions=param_dist,
    )
    model.fit(features, target)
    joblib.dump(model, "model-test.joblib")
    return model.best_score_, model.best_estimator_


def make_model():
    features, target = get_data()
    model = RandomForestClassifier(
        criterion="entropy",
        max_depth=11,
        n_estimators=299,
        n_jobs=8,
        random_state=42,
    )
    model.fit(features, target)
    joblib.dump(model, "model.joblib")


if __name__ == '__main__':
    # print(find_best_fit())
    make_model()
