import random
from .cities_collection import CitiesCollection
from .images_getter import ImageGetterCached

def shuffle_copy(lst):
    random.shuffle(lst.copy())
    return lst


class Question(object):
    def __init__(self, text, perk, min_, max_):
        self.question_text = text
        self.question_perk = perk
        self.min = min_
        self.max = max_

    def to_json(self):
        return {
            'question_text': self.question_text,
            'question_perk': self.question_perk,
            'min': self.min,
            'max': self.max
        }


class CityQuestion(object):
    def __init__(self, city1, city2, url1, url2):
        self.city1_name = city1
        self.city2_name = city2
        self.city1 = url1
        self.city2 = url2

    def to_json(self):
        return {
            'city1_name': self.city1_name,
            'city2_name': self.city2_name,
            'city1': self.city1,
            'city2': self.city2
        }


class CitiesFunnel:
    def __init__(self, img_getter):
        self.cities_collection = CitiesCollection()
        self.img_getter = img_getter
        self.cities_set = set(self.cities_collection.get_cities())
        self.data = self.cities_collection.data
        self.static_features = shuffle_copy(self.cities_collection.get_features())
        self.feature_scores = {}
        self.current_static_feature_idx = 0

    def get_cities_pair(self):
        return random.sample(self.cities_collection.get_cities(), 2)

    def _get_next_static_feature(self):
        if self.current_static_feature_idx >= len(self.static_features):
            raise RuntimeError("not enough static features")
        result = self.static_features[self.current_static_feature_idx]
        self.current_static_feature_idx += 1
        return result

    def _get_next_dynamic_feature(self):
        return self.get_cities_pair()

    def get_next_question(self):
        if bool(random.getrandbits(1)):
            feature = self._get_next_static_feature()
            min_, max_ = self.cities_collection.get_range(feature)
            return Question(self.cities_collection.get_question(feature), feature, min_, max_)
        else:
            city1, city2 = self._get_next_dynamic_feature()
            url1, url2 = self.img_getter.get_random_imgs(city1, city2)
            return CityQuestion(city1, city2, url1, url2)

    def set_rating(self, feature, rating):
        city_scale = 0.3
        self.feature_scores[feature] = rating * (city_scale if feature in self.cities_set else 1)
        return self._filter_cities(feature)

    def compute_scores(self):
        def compute_score(row):
            return sum([abs(val - (0 if key in self.cities_set else row[key])) for key, val in self.feature_scores.items()])
        self.data['score'] = self.data.apply(compute_score, axis=1)

    def find_best(self, count):
        self.compute_scores()
        return self.data.sort_values(by=['score'])['country'].iloc[:count].values

    def _filter_cities(self, feature):
        d = self.data
        delta = 3
        min_valuable_count = 3
        if feature not in self.cities_set:
            self.data = self.data[(d[feature] > self.feature_scores[feature] - delta) & (d[feature] < self.feature_scores[feature] + delta)]
        # it will fail there
        if len(self.data) <= min_valuable_count:
            return self.find_best(min_valuable_count)
        return None
