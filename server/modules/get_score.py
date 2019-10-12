import pandas as pd
import numpy as np
from .cities_collection import CitiesCollection


class ScoreCalculator():
    def __init__(self, answers):
        self.cities_collection = CitiesCollection()
        self.answers = answers
        self.new_data = self.cities_collection.data
        self.scores = [0] * self.new_data.shape[0]

    def get_city_recommendation(self, n_cities=10):
        for index, row in self.new_data.iterrows():
            for key, value in self.answers.items():
                try:
                    self.scores[index] += abs(
                        int(row[self.cities_collection._old_new_features_mapping[key]]) - int(value))
                    print(self.scores[index], int(row[self.cities_collection._old_new_features_mapping[key]]),
                          int(value))
                except ValueError as e:
                    self.scores[index] += int(value)

        # self.new_data.to_csv("test.csv")
        self.scores.reverse()
        cities = np.argpartition(
            np.array(self.scores), -1 * n_cities)[-1 * n_cities:]
        print(self.scores)
        cities = np.array(self.cities_collection.get_cities())[cities]

        print(cities)
        return cities

        cities = np.array(self.cities_collection.get_cities())[cities]

        print(cities)
