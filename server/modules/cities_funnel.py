import random
from .cities_collection import CitiesCollection


class CitiesFunnel:
    def __init__(self):
        self.cities_collection = CitiesCollection()
        self.static_features = random.shuffle(self.cities_collection.get_features())
        self.current_feature_idx = 0
        self.cities = self.cities_collection.get_cities()

    def get_next_static_feature(self):
        if self.current_feature_idx >= len(self.static_features):
            raise RuntimeError("not enough static features")
        result = self.static_features[self.current_feature_idx]
        self.current_feature_idx += 1
        return result

    def get_next_feature(self):
        return self.get_next_static_feature()
