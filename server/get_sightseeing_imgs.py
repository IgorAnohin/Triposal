import configparser

from modules.cities_collection import CitiesCollection
from modules.images_getter import ImageGetter
import pandas as pd
import time
from tqdm import tqdm


CONFIG_FP = 'config.conf'


def get_sightseing_urls(img_getter, city, keyword):
    time.sleep(3.33)
    return img_getter.get(city, keyword, count=10)


def read_from_file(keyword):
    df = pd.read_csv('data/{}.csv'.format(keyword))
    return df.drop(['Unnamed: 0'], axis=1).to_dict(orient='records')


def grab_imgs(img_getter, cities, keyword):
    rows = read_from_file(keyword)
    for city in tqdm(cities[len(rows):]):
        try:
            urls = get_sightseing_urls(img_getter, city, keyword)
        except RuntimeError as e:
            print(e)
            return rows
        rows.append({
            'city': city,
            'keyword': keyword,
            'urls': ' '.join(urls)
        })
    return rows


def main():
    config = configparser.ConfigParser()
    config.read(CONFIG_FP)

    cities = CitiesCollection().get_cities()

    img_getter = ImageGetter(config['google.api']['developer_key'], config['google.api']['cx'])

    for key_word in ['sightseeing', 'nature', 'dish']:
        rows = grab_imgs(img_getter, cities, key_word)
        df = pd.DataFrame(rows)
        df.to_csv('data/{}.csv'.format(key_word))


if __name__ == '__main__':
    main()
