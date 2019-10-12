from google_images_search import GoogleImagesSearch


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
        for image in gis.results():
            print(image.url)

        return 0
