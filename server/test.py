
from modules.cities_funnel import CitiesFunnel


def test():
    funnel = CitiesFunnel()
    feature = funnel.get_next_feature()
    funnel.set_rating(feature, 3)
    res = funnel.find_best()
    print('feature', feature)
    print('res', res)


if __name__ == '__main__':
    test()
