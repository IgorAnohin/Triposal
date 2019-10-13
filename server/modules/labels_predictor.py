from google.cloud import vision
import time
import pickle
import pandas as pd


class LabelPredictor:
    available_labels = ['Landmark', 'Architecture', 'Building', 'City', 'Sky', 'Human settlement', 'Tourism', 'Town', 'Historic site', 'Metropolitan area']

    def load_cache(self):
        df = pd.read_csv("ml_engine/ml_engine_cache.csv")
        for idx, row in df.iterrows():
            self._cache[row['url']] = [row[lbl] for lbl in self.available_labels]

    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        self._cache = {}
        self.load_cache()

    def get_labels(self, url):
        time.sleep(1.5)
        try:
            resp = self.client.annotate_image({
                'image': {'source': {'image_uri': url}},
                'features': [{'type': vision.enums.Feature.Type.LABEL_DETECTION}],
            })

            return {ann.description: ann.score for ann in resp.label_annotations}
        except RuntimeError as e:
            print(e)
            return {}

    def get_labels_vector(self, url):
        features = self.get_labels(url)
        scores = [features.get(lbl, 0) for lbl in self.available_labels]
        return scores

    def get_from_cache(self, url):
        return self._cache.get(url, [0 for _ in self.available_labels])
