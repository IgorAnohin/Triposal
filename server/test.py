import configparser
from modules.cities_funnel import CitiesFunnel
from modules.price_finder import PriceFinder
from modules.images_getter import ImageGetterLocal


def test():
    funnel = CitiesFunnel()
    label, feature = funnel.get_next_feature()
    funnel.set_rating(feature, 3)
    res = funnel.find_best()
    print('feature', feature)
    print('res', res)


if __name__ == '__main__':
    # test()
    # CONFIG_FP = 'config.conf'
    # config = configparser.ConfigParser()
    # config.read(CONFIG_FP)
    # price_finder = PriceFinder(config['skyscanner.api']['api_key'])
    # asd = price_finder.get_price("spain", max_results=1)[0]['MinPrice']
    # print(asd)

    getter = ImageGetterLocal()
    result = getter.get_random()
    print('result', result)
