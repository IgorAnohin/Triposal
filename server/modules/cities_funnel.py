import random
from .cities_collection import CitiesCollection
from .images_getter import ImageGetterCached
from .labels_predictor import LabelPredictor
import logging
import pickle
import pandas as pd


def shuffle_copy(lst):
    random.shuffle(lst.copy())
    return lst


class QuestionScored(object):
    def __init__(self, text, perk, min_, max_, image_):
        self.question_text = text
        self.question_perk = perk
        self.min = min_
        self.max = max_
        self.image = image_

    def to_json(self):
        json = {
            'type': 'numeric',
            'question_text': self.question_text,
            'question_perk': self.question_perk,
            'min': self.min,
            'max': self.max,
            'image': self.image
        }
        print('JSON\n', json)
        return json


class QuestionBinary(object):
    def __init__(self, text, perk, image_):
        self.question_text = text
        self.question_perk = perk
        self.image = image_

    def to_json(self):
        json = {
            'type': 'binary',
            'question_text': self.question_text,
            'question_perk': self.question_perk,
            'image': self.image
        }
        print(json)
        return json


class CityQuestion(object):
    def __init__(self, city1, city2, url1, url2):
        self.city1_name = city1
        self.city2_name = city2
        self.city1 = url1
        self.city2 = url2

    def get_url(self, city):
        if city == self.city1_name:
            return self.city1
        else:
            return self.city2

    def to_json(self):
        json = {
            'city1_name': self.city1_name,
            'city2_name': self.city2_name,
            'city1': self.city1,
            'city2': self.city2
        }
        print(json)
        return json


class CitiesFunnel:
    def _get_available_cities(self):
        return pd.read_csv('data/sightseeing.csv')['city'].tolist()

    def init(self):
        self.data = self.cities_collection.data.copy()
        self.static_scored_features = shuffle_copy(self.cities_collection.get_scored_features())
        self.static_binary_features = shuffle_copy(self.cities_collection.get_binary_features())
        self.feature_scores = {}
        self.current_static_scored_feature_idx = 0
        self.current_static_binary_feature_idx = 0

    def load_ml_model(self):
        path = 'ml_engine/model.pickle'
        return pickle.load(open(path, 'rb'))

    def get_target_prediction(self):
        return self.model.prediction(self.ml_vector) * self.ml_scale

    def cumulate_ml_vector(self, url_img):
        alpha = 0.8
        next_vector = self.label_vector.get_from_cache(url_img)
        self.ml_vector = self.ml_vector * alpha + next_vector * (1. - alpha)

    def get_cities_predictions(self):
        idx_to_classes = self.model.classes_

        vector = [0] * len(self.cities_set)
        city_to_idx = {city: idx for idx, city in enumerate(self.cities_set)}

        self.ml_cities_predictions = self.model.predict_proba(pd.DataFrame([self.ml_vector]))[0]
        for idx, score in enumerate(self.ml_cities_predictions):
            vector[city_to_idx[idx_to_classes[idx]]] = score
        self.ml_cities_predictions = vector

    def __init__(self, img_getter, use_ml=False):
        self.cities_collection = CitiesCollection(self._get_available_cities())
        self.img_getter = img_getter
        self.cities_set = set(self.cities_collection.get_cities())
        self.use_ml = use_ml
        self.ml_scale = 0.2
        self.ml_vector = None
        self.ml_cities_predictions = None
        self.label_vector = LabelPredictor()
        self.model = self.load_ml_model() if self.use_ml else None

        self.data = None
        self.static_scored_features = None
        self.static_binary_features = None
        self.feature_scores = None
        self.current_static_binary_feature_idx = None
        self.current_static_scored_feature_idx = None
        self.init()

    def get_cities_pair(self):
        return random.sample(self.cities_collection.get_cities(), 2)

    def _get_next_static_scored_feature(self):
        if self.current_static_scored_feature_idx >= len(self.static_scored_features):
            raise RuntimeError("not enough static scored features")
        result = self.static_scored_features[self.current_static_scored_feature_idx]
        self.current_static_scored_feature_idx += 1
        return result

    def _get_next_static_binary_feature(self):
        if self.current_static_binary_feature_idx >= len(self.static_binary_features):
            raise RuntimeError("not enough static binary features")
        result = self.static_binary_features[self.current_static_binary_feature_idx]
        self.current_static_binary_feature_idx += 1
        return result

    def _get_next_dynamic_feature(self):
        return self.img_getter.get_random()

    def get_next_question(self):
        rand_val = random.randrange(3)
        if rand_val == 0:
            feature = self._get_next_static_scored_feature()
            min_, max_ = self.cities_collection.get_range(feature)
            return QuestionScored(self.cities_collection.get_numeric_question(feature), feature, min_, max_,
                                  self.cities_collection.get_image(feature))
        elif rand_val == 1:
            city1, city2, url1, url2 = self._get_next_dynamic_feature()
            return CityQuestion(city1, city2, url1, url2)
        else:
            feature = self._get_next_static_binary_feature()
            return QuestionBinary(self.cities_collection.get_binary_question(feature), feature,
                                  self.cities_collection.get_image(feature))

    def set_rating(self, feature, rating, url_img=None):
        if self.use_ml and feature in self.cities_set and (url_img is not None):
            self.cumulate_ml_vector(url_img)

        city_scale = 0.3
        self.feature_scores[feature] = rating * (city_scale if feature in self.cities_set else 1)
        print('FEATURE SCORES')
        print(self.feature_scores)
        return self._filter_cities(feature)

    def compute_scores(self):
        city_to_idx = {city: idx for idx, city in enumerate(self.cities_set)}

        def compute_ml_factor(city):
            if self.use_ml:
                self.get_cities_predictions()
            vector = [0] * len(self.cities_set)
            vector[city_to_idx[city]] = 1
            return (sum([(x - y)**2 for x, y in zip(self.ml_cities_predictions, vector)]))**0.5 * self.ml_scale

        def compute_score(row):
            return sum(
                [abs(val - (0 if city in self.cities_set else row[city])) + compute_ml_factor(city) for city, val in self.feature_scores.items()])

        self.data['score'] = self.data.apply(compute_score, axis=1)

    def find_best(self, count):
        self.compute_scores()
        return self.data.sort_values(by=['score'])['city'].iloc[:count].values

    def _filter_cities(self, feature):
        d = self.data
        delta = 3
        min_valuable_count = 3
        changed = False
        if feature not in self.cities_set:
            new_data = self.data[(d[feature] > self.feature_scores[feature] - delta) & (
                    d[feature] < self.feature_scores[feature] + delta)]
            if len(new_data) > min_valuable_count:
                changed = True
                self.data = new_data
        # it will fail there
        if len(self.data) <= min_valuable_count or (not changed):
            top_scores = self.find_best(min_valuable_count)
            print('TOP SCORES')
            print(top_scores)
            return top_scores
        return None

    def reset(self):
        self.init()
