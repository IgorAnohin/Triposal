import configparser

from requests.exceptions import ConnectionError, ReadTimeout
from modules.cities_collection import CitiesCollection
from modules.images_getter import ImageGetter
import pandas as pd
import time
from tqdm import tqdm


def read_from_file(keyword):
    df = pd.read_csv('data/{}.csv'.format(keyword))
    return df.drop(['Unnamed: 0'], axis=1).to_dict(orient='records')


def main():
    config = configparser.ConfigParser()
    config.read('config.conf')

    cities = CitiesCollection(pd.read_csv('data/sightseeing.csv')['city'].tolist()).get_cities()

    getter = ImageGetter(config['google.api']['developer_key'], config['google.api']['cx'])

    for key_word in ['dish']:  # nature
        rows = read_from_file(key_word)
        start_idx = len(rows) + 4

        for city in tqdm(cities[start_idx:]):
            time.sleep(1.5)
            try:
                urls = getter.get(city, key_word)
                rows.append({
                    'city': city,
                    'keyword': key_word,
                    'urls': ' '.join(urls)
                })
            except ConnectionError as e:
                print(e)
            df = pd.DataFrame(rows)
            df.to_csv('data/{}.csv'.format(key_word))


if __name__ == '__main__':
    main()
