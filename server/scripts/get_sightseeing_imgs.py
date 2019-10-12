import configparser
from ..modules.images_getter import ImageGetter


CONFIG_FP = 'config.conf'


def get_sightseing_urls(img_getter, city, keyword):
    return img_getter.get(city, keyword, count=10)


def grab_imgs(img_getter, cities, keyword):
    rows = []
    for city in cities:
        urls = get_sightseing_urls(img_getter, cities, keyword)

        rows.append({
            'city': city,
            'urls': ' '.join(urls)
        })


def main():
    pass
    # config = configparser.ConfigParser()
    # config.read(CONFIG_FP)
    #
    # # cities =
    #
    # img_getter = ImageGetter(config['google.api']['developer_key'], config['google.api']['cx'])
    #
    # key_words = ['sightseeing', 'celebrity', 'famous dish']
    # grab_imgs(img_getter, cities, key_words[0])




if __name__ == '__main__':
    main()
