from google_images_search import GoogleImagesSearch
import configparser


class ImageGetter:
    CONFIG_FP = 'config.conf'

    def __init__(self, developer_key):
        self._config = configparser.ConfigParser()
        self._config.read(self.CONFIG_FP)

    def get(self, city, count=4):
        gis = GoogleImagesSearch(self._config['google.api']['developer_key'], self._config['google.api']['cx'])
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


if __name__ == '__main__':
    img_getter = ImageGetter()
    imgs = img_getter.get("Istanbul")
    print(imgs)
