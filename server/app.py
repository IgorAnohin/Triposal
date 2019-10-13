import configparser

from flask import Flask, jsonify, request
from datetime import datetime

from modules.images_getter import ImageGetterCached, ImageGetterLocal
from modules.price_finder import PriceFinder
from modules.cities_funnel import CitiesFunnel

USE_ML = False
city_question = None

CONFIG_FP = 'config.conf'
config = configparser.ConfigParser()
config.read(CONFIG_FP)

app = Flask(__name__)

img_getter = ImageGetterLocal()
funnel = CitiesFunnel(img_getter, USE_ML)
price_finder = PriceFinder(config['skyscanner.api']['api_key'])


def choose_greeting():
    # Where to next?
    today = datetime.now().strftime("%H:%M")
    if '05:00' <= today < '12:00':
        return 'Good morning!'
    elif '12:00' <= today < '18:00':
        return 'Good afternoon!'
    return 'Good evening!'


def form_web_url():
    url = 'https://www.skyscanner.es/transport/flights/bcn/{dest_city}/{from_date}/{to_date}/'\
        .format(dest_city='fran', from_date='191017', to_date='191024')
    urlWithParams = url + '?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home#/'
    return urlWithParams


def merge_with_flights(cities):
    print('cities', cities)
    flights = [price_finder.get_price(city, max_results=1)[0] for city in cities]
    min_prices = [flight['MinPrice'] if len(flight) > 0 else 0 for flight in flights]
    booking_urls = [flight['booking_url'] for flight in flights]
    urls = [img_getter.get_random_url('sightseeing', city) for city in cities]
    return [{'city': city, 'min_price': min_price, 'url': url, 'booking_url': booking_url} for (city, min_price, url, booking_url) in zip(cities, min_prices, urls, booking_urls)]


@app.route('/greeting', methods=['GET'])
def get_greeting():
    return jsonify({'greeting': choose_greeting()})


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        global city_question
        city_question = funnel.get_next_question()
        return jsonify(city_question.to_json())
    elif request.method == 'POST':
        import json
        print("request.data", request.data)
        print('request.json', request.json)
        print("request", request.__dict__)

        d = json.loads(request.data)
        if 'city' in d:
            feature = d.get('city')
            score = 1
            url = city_question.get_url(feature)
        else:
            feature = d.get('question_perk')
            score = int(d.get('value'))
            url = None

        resulted_cities = funnel.set_rating(feature, score, url)
        json = {'status': 'confirmed'}
        if resulted_cities is not None:
            json['flights'] = merge_with_flights(resulted_cities)
        return jsonify(json)


@app.route('/reset', methods=['POST'])
def reset():
    funnel.reset()
    return jsonify({'status': 'confirmed'})


@app.route('/final', methods=['GET'])
def final_result():
    cities = funnel.find_best(3)
    return jsonify({'flights': merge_with_flights(cities)})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
