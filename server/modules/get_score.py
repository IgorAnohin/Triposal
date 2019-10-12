import pandas as pd
import numpy as np
from .cities_collection import CitiesCollection


class ScoreCalculator():
    def __init__(self, answers):
        self.cities_collection = CitiesCollection()
        self.answers = answers
        scores = pd.DataFrame(
            {'score': [0] * 730})
        self.new_data = pd.concat([self.cities_collection.data, scores], sort=False)
        self.new_data.to_csv("test2.csv")

    def get_city_recommendation(self, n_cities=10):
        for index, row in self.new_data.iterrows():
            for key, value in self.answers.items():
                try:
                    row['score'] += int(
                        row[self.cities_collection._old_new_features_mapping[key]]) - int(value)
                except ValueError as e:
                    row['score'] += int(value)

        # self.new_data.to_csv("test.csv")
        cities = np.argpartition(
            self.new_data['score'].to_numpy(), -1 * n_cities)[-1 * n_cities:]

        cities = np.array(self.cities_collection.get_cities())[cities]

        print(cities)