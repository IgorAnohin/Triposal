from lightgbm import LGBMClassifier
import pickle
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def read_dataset():
    path = 'image_labels.pickle'
    d = pickle.load(open(path, 'rb'))
    return d


def dump_model(model, fp='model.pickle'):
    pickle.dump(model, open(fp, 'wb'))


def dump_features(features, fp='ml_cache.csv'):
    pd.DataFrame(features).to_csv(fp, index=False)


def get_url_country_mapping():
    path = '../data/sightseeing.csv'
    df = pd.read_csv(path)
    url_to_city = {}
    for idx, row in df.iterrows():
        urls = row['urls'].split(' ')
        for url in urls:
            url_to_city[url] = row['city']
    return url_to_city


def label_counter(d):
    labels = []
    for _, val in d.items():
        labels += [elem['description'] for elem in val]
    return Counter(labels)


def get_labels(counters: Counter, count=10):
    labels = counters.most_common(count)
    return [label[0] for label in labels]


def compute_features(d, labels, url_city_mapping):
    df = []
    for url, ann in d.items():
        mapping = {x['description']: x['score'] for x in ann}
        city = url_city_mapping[url]
        df.append([mapping.get(label, 0) for label in labels] + [city])
    return df


def train_and_learn(features):
    available_labels = ['Landmark', 'Building', 'City', 'Human settlement', 'Public space', 'Town square', 'Town',
                        'Plaza', 'Architecture', 'Metropolitan area']
    lgbm = LGBMClassifier(n_estimators=10, silent=False, random_state=94, max_depth=5, num_leaves=31, objective='binary', metrics='auc')

    y = features['city']
    features = features.drop(['city'], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.33, random_state=42)

    model = lgbm.fit(X_train, y_train)
    predicts = model.predict(X_test)
    # print(predicts)
    print(model.predict_proba(pd.DataFrame([{av_lbl: 0.2 for av_lbl in available_labels}]))[0])
    print('classes_', model.classes_)
    acc = accuracy_score(y_test, predicts)
    # print(acc)
    return model


def train_and_dump():
    d = read_dataset()
    counters = label_counter(d)
    labels = get_labels(counters)

    df = []
    for url, ann in d.items():
        mapping = {x['description']: x['score'] for x in ann}
        df.append([mapping.get(label, 0) for label in labels] + [url])
    df = pd.DataFrame(df, columns=labels + ['url'])
    df.to_csv("ml_engine_cache.csv")

    url_city_mapping = get_url_country_mapping()
    features = compute_features(d, labels, url_city_mapping)
    features = pd.DataFrame(features, columns=labels + ['city'])

    lgbm = LGBMClassifier(n_estimators=10, silent=False, random_state=94, max_depth=5, num_leaves=31,
                          objective='binary', metrics='auc')
    y = features['city']
    features = features.drop(['city'], axis=1)
    model = lgbm.fit(features, y)
    dump_model(model)


def main():
    d = read_dataset()
    counters = label_counter(d)
    labels = get_labels(counters)
    print(labels)

    url_city_mapping = get_url_country_mapping()
    features = compute_features(d, labels, url_city_mapping)
    features = pd.DataFrame(features, columns=labels + ['city'])

    model = train_and_learn(features)


if __name__ == '__main__':
    # train_and_dump()
    main()
