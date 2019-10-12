import pandas as pd


class CitiesCollection:
    DEFAULT_FP = "data/cities_predict.csv"

    def _preprocess_data(self, data):
        def prettify_place(row):
            return ' '.join(map(lambda s: s.capitalize(), row['place_slug'].split('-')[:-row['countries_parts']]))

        data['countries_parts'] = data['country'].str.split().str.len()
        data['city'] = data[['place_slug', 'countries_parts']].apply(prettify_place, axis=1)
        data = data.rename(columns=self._old_new_features_mapping)
        data = data[self._key_features + self._features]
        return data

    def _load_table(self, filepath):
        data = pd.read_csv(filepath)
        return self._preprocess_data(data)

    # should be like this (not parsing) due to some strange column names (not in the list right now)
    @staticmethod
    def _get_old_new_features_mapping():
        return {
            'female_friendly': 'female friendly',
            'freedom_of_speech': 'freedom of speech',
            'friendly_to_foreigners': 'friendly to foreigners',
            'fun': 'fun',
            'happiness': 'happiness',
            'healthcare': 'healthcare',
            'lgbt_friendly': 'lgbt friendly',
            'nightlife': 'nightlife',
            'peace': 'peace',
            'quality_of_life': 'quality of life',
            'racial_tolerance': 'racial tolerance',
            'religious_government': 'religious government',
            'safety': 'safety',
            'startup_score': 'startup score',
            'traffic_safety': 'traffic safety',
            'walkability': 'walkability'
        }

    def get_main_features(self):
        return ['region', 'country', 'city']

    # only exceptional (!= (0, 5))
    @staticmethod
    def _get_features_ranges_mapping():
        return {}

    def get_cities(self):
        return list(self.data['city'])

    def get_countries(self):
        return list(self.data['country'])

    def get_features(self):
        return self._features

    def get_range(self, feature):
        return self._features_ranges_mapping.get(feature, (1, 5))

    def __init__(self):
        self._old_new_features_mapping = self._get_old_new_features_mapping()
        self._features = list(self._old_new_features_mapping.values())

        self._key_features = self.get_main_features()
        self._features_ranges_mapping = self._get_features_ranges_mapping()

        self.data = self._load_table(self.DEFAULT_FP)
