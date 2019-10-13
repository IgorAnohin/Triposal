import configparser
from modules.cities_funnel import CitiesFunnel
from modules.price_finder import PriceFinder
from modules.images_getter import ImageGetter
import datetime


def get_last_week(fmt='%y%m%d'):
    today = datetime.datetime.now()
    next_week = (today + datetime.timedelta(days=7)).strftime(fmt)
    next_week2 = (today + datetime.timedelta(days=14)).strftime(fmt)
    return next_week, next_week2


def form_web_url(dest_city='fran'):
    from_date, to_date = get_last_week('%y%m%d')
    url = 'https://www.skyscanner.es/transport/flights/bcn/{dest_city}/{from_date}/{to_date}/'\
        .format(dest_city=dest_city, from_date=from_date, to_date=to_date)
    urlWithParams = url + '?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home#/'
    return urlWithParams


def test():
    funnel = CitiesFunnel()
    label, feature = funnel.get_next_feature()
    funnel.set_rating(feature, 3)
    res = funnel.find_best()
    print('feature', feature)
    print('res', res)


def test1():
    config = configparser.ConfigParser()
    config.read('config.conf')

    getter = ImageGetter(config['google.api']['developer_key'], config['google.api']['cx'])
    asd = getter.get('toronto', 'sightseeing')


def test2():
    config = configparser.ConfigParser()
    config.read('config.conf')
    price_finder = PriceFinder(config['skyscanner.api']['api_key'])
    prices = price_finder.get_price(to_city_name='toronto')
    print('prices')
    print(prices)
    url = form_web_url('toronto')
    print('URL:\n')
    print(url)



if __name__ == '__main__':
    test2()
