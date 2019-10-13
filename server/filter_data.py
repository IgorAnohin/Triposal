import pandas as pd


def get_default_cities():
    def prettify_place(row):
        return ' '.join(map(lambda s: s.capitalize(), row['place_slug'].split('-')[:-row['countries_parts']]))

    data = pd.read_csv('data/cities_predict.csv')
    data['countries_parts'] = data['country'].str.split().str.len()
    data['city'] = data[['place_slug', 'countries_parts']].apply(prettify_place, axis=1)
    return set(data['city'].tolist())


def remove_least_valuable_cities():
    sightseeing = pd.read_csv('data/sightseeing.csv')
    sightseeing = sightseeing.dropna(axis=0)

    true_cities = sightseeing['city'].tolist()
    default_cities = get_default_cities()
    true_cities = filter(lambda x: x not in default_cities, true_cities)

    nature = pd.read_csv('data/nature.csv').dropna(axis=0)
    nature = nature[nature['city'].isin(true_cities)]

    dish = pd.read_csv('data/dish.csv').dropna(axis=0)
    dish = dish[dish['city'].isin(true_cities)]

    sightseeing.to_csv('data/sightseeing.csv', index=False)
    nature.to_csv('data/nature.csv', index=False)
    dish.to_csv('data/dish.csv', index=False)


def remove_bad_uri_links():
    cities = pd.read_csv('data/sightseeing.csv')
    nature = pd.read_csv('data/nature.csv')
    dish = pd.read_csv('data/dish.csv')


def main():
    remove_least_valuable_cities()

main()
