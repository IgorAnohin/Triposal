import pandas as pd


def remove_least_valuable_cities():
    sightseeing = pd.read_csv('data/sightseeing.csv')
    sightseeing = sightseeing.dropna(axis=0)
    true_cities = sightseeing['city'].tolist()

    nature = pd.read_csv('data/nature.csv').dropna(axis=0)
    nature = nature[nature['city'].isin(true_cities)]

    dish = pd.read_csv('data/dish.csv').dropna(axis=0)
    dish = dish[dish['city'].isin(true_cities)]

    sightseeing.to_csv('data/sightseeing_v2.csv', index=False)
    nature.to_csv('data/nature_v2.csv', index=False)
    dish.to_csv('data/dish_v2.csv', index=False)


def remove_bad_uri_links():
    cities = pd.read_csv('data/sightseeing.csv')
    nature = pd.read_csv('data/nature.csv')
    dish = pd.read_csv('data/dish.csv')


def main():
    remove_least_valuable_cities()

main()
