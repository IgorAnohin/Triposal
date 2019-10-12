import random
from .cities_collection import CitiesCollection


def shuffle_copy(lst):
    random.shuffle(lst.copy())
    return lst


class CitiesFunnel:
    def __init__(self):
        self.cities_collection = CitiesCollection()
        self.cities_set = set(self.cities_collection.get_cities())
        self.data = self.cities_collection.data
        self.static_features = shuffle_copy(self.cities_collection.get_features())
        self.dynamic_features = shuffle_copy(self.cities_collection.get_cities())
        self.feature_scores = {}
        self.current_static_feature_idx = 0
        self.current_dynamic_feature_idx = 0

    def _get_next_static_feature(self):
        if self.current_static_feature_idx >= len(self.static_features):
            raise RuntimeError("not enough static features")
        result = self.static_features[self.current_static_feature_idx]
        self.current_static_feature_idx += 1
        return result

    def _get_next_dynamic_feature(self):
        result = self.dynamic_features[self.current_dynamic_feature_idx % len(self.dynamic_features)]
        self.current_dynamic_feature_idx += 1
        return result

    def get_next_feature(self):
        if bool(random.getrandbits(1)):
            return self._get_next_static_feature()
        else:
            return self._get_next_dynamic_feature()

    def set_rating(self, feature, rating):
        city_scale = 0.3
        self.feature_scores[feature] = rating * (city_scale if feature in self.cities_set else 1)
        self._filter_cities(feature)

    def compute_scores(self):
        def compute_score(row):
            return sum([abs(val - (0 if key in self.cities_set else row[key])) for key, val in self.feature_scores.items()])
        self.data['score'] = self.data.apply(compute_score, axis=1)

    def find_best(self):
        self.compute_scores()
        return self.data.loc[self.data['score'].idxmin()]['country']

    def _filter_cities(self, feature):
        d = self.data
        delta = 3
        min_valuable_count = 3
        if feature not in self.cities_set:
            self.data = self.data[(d[feature] > self.feature_scores[feature] - delta) & (d[feature] < self.feature_scores[feature] + delta)]
        # it will fail there
        if len(self.data) < min_valuable_count:
            return self.find_best()
        return None
