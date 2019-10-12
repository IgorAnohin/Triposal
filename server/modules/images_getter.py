from google_images_search import GoogleImagesSearch
import pickle
import os.path
import random


class ImageGetter:
    def __init__(self, developer_key, cx):
        self._developer_key = developer_key
        self._cx = cx

    def get(self, city, count=4):
        gis = GoogleImagesSearch(self._developer_key, self._cx)
        search_params = {
            'q': '{} sightseeing'.format(city),
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

    def get(self, city, count=4):
        if city in self._cache:
            response = self._cache[city]
            if response[0] >= count:
                # we are good
                return response[1]
        self.increase_cache_idx()
        result = super().get(city, count)
        self._cache[city] = (max(count, len(result)), result)
        if self._cache_idx >= self.CACHE_DUMP_IDX:
            self._dump_cache()
        return result

    def get_random_imgs(self, lhs, rhs):
        urls_lhs = self.get(lhs)
        urls_rhs = self.get(rhs)
        urls = [self._get_random(urls_lhs), self._get_random(urls_rhs)]
        return urls
