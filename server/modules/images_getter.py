from google_images_search import GoogleImagesSearch
import pickle
import os.path
import random
import pandas as pd


class ImageGetter:
    def __init__(self, developer_key, cx):
        self._developer_key = developer_key
        self._cx = cx

    def get(self, request, key_word, count=4):
        gis = GoogleImagesSearch(self._developer_key, self._cx)
        search_params = {
            'q': '{} {}'.format(request, key_word),
            'num': count,
            'fileType': 'jpg',
            'imgType': 'photo'  # 'huge|icon|large|medium|small|xlarge|xxlarge'
        }
        gis.search(search_params=search_params)
        return [image.url for image in gis.results()]


class ImageGetterCached(ImageGetter):
    CACHE_FP = 'data/img_cache.pickle'
    CACHE_DUMP_IDX = 10

    # cache structure:
    # country: (count, [url1, url2, url3, ...])

    def _read_cache(self):
        if os.path.isfile(self.CACHE_FP):
            self._cache = pickle.load(open(self.CACHE_FP, 'rb'))
        else:
            self._cache = {}

    def _get_random(self, urls):
        return random.choice(urls)

    def _dump_cache(self):
        self._cache_idx = 0
        pickle.dump(self._cache, open(self.CACHE_FP, 'wb'))

    def increase_cache_idx(self):
        self._cache_idx += 1

    def __init__(self, developer_key, cx):
        super().__init__(developer_key, cx)
        self._read_cache()
        self._cache_idx = 0

    def get(self, request, key_word, count=4):
        if (request, key_word) in self._cache:
            response = self._cache[(request, key_word)]
            if response[0] >= count:
                # we are good
                return response[1]
        self.increase_cache_idx()
        result = super().get(request, key_word, count)
        self._cache[(request, key_word)] = (max(count, len(result)), result)
        if self._cache_idx >= self.CACHE_DUMP_IDX:
            self._dump_cache()
        return result

    def get_random_key_word(self):
        key_words = ['sightseeing', 'celebrity', 'famous dish']
        return random.choice(key_words)

    def get_random_imgs(self, lhs, rhs, key_word=None):
        if key_word is None:
            key_word = self.get_random_key_word()
        urls_lhs = self.get(lhs, key_word)
        urls_rhs = self.get(rhs, key_word)
        return self._get_random(urls_lhs), self._get_random(urls_rhs)


class ImageGetterLocal:
    key_words = ['sightseeing', 'nature', 'dish']

    def __init__(self):
        self.dfs = {key_word: pd.read_csv('data/{}.csv'.format(key_word)) for key_word in self.key_words}
        self.cities = {key_word: self.dfs[key_word]['city'].tolist() for key_word in self.key_words}

    def get_random_key_word(self):
        return random.choice(self.key_words)

    def get_random_url(self, key_word, city):
        print("CITY", city)
        df = self.dfs[key_word]
        print('df')
        print(df[df['city'] == city])
        city_data = df[df['city'] == city].iloc[0]
        return random.sample(city_data['urls'].split(' '), 1)[0]

    def get_random(self):
        key_word = self.get_random_key_word()
        city1, city2 = random.sample(self.cities[key_word], 2)
        url1, url2 = self.get_random_url(key_word, city1), self.get_random_url(key_word, city2)
        return city1, city2, url1, url2
