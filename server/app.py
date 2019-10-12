import configparser
import random

from flask import Flask, jsonify, request

from modules.images_getter import ImageGetterCached
from modules.get_score import ScoreCalculator
from modules.price_finder import PriceFinder

app = Flask(__name__)

CONFIG_FP = 'config.conf'

questions = [
    {'question_text': 'How family friendly should the city be?', 'question_perk': 'female_friendly', 'min': 0,
     'max': 5},
    {'question_text': 'How fun should be the city?', 'question_perk': 'fun', 'min': 0, 'max': 5},
    {'question_text': 'Happiness level of the city?', 'question_perk': 'happiness', 'min': 0, 'max': 5},
    {'question_text': 'Healthcare level in the city?', 'question_perk': 'healthcare', 'min': 0, 'max': 5},
    {'question_text': 'Should the city be LGBT friendly?', 'question_perk': 'lgbt_friendly', 'min': 0, 'max': 5},
    {'question_text': 'Nightlife activity in the city.', 'question_perk': 'nightlife', 'min': 0, 'max': 5},
    {'question_text': 'How peaceful is the city required to be?', 'question_perk': 'peace', 'min': 0, 'max': 5},
    {'question_text': 'Tolerance level towards non-local races?', 'question_perk': 'racial_tolerance', 'min': 0,
     'max': 5},
    {'question_text': 'How religious should be the government?', 'question_perk': 'religious_government', 'min': 0,
     'max': 5},
    {'question_text': 'Required safety level?', 'question_perk': 'safety', 'min': 0, 'max': 5},
    {'question_text': 'How good is the city for developing a startup?', 'question_perk': 'startup_score', 'min': 0,
     'max': 5},
    {'question_text': 'How safe is the traffic?', 'question_perk': 'traffic_safety', 'min': 0, 'max': 5},
    {'question_text': 'How good is the city for walks?', 'question_perk': 'walkability', 'min': 0, 'max': 5}]

city_perks = {'female_friendly': 0,
              'fun': 0,
              'happiness': 0,
              'healthcare': 0,
              'lgbt_friendly': 0,
              'nightlife': 0,
              'peace': 0,
              'racial_tolerance': 0,
              'religious_government': 0,
              'safety': 0,
              'startup_score': 0,
              'traffic_safety': 0,
              'walkability': 0}


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        rand_val = random.randrange(2)
        if rand_val == 0:
            return next_question()
        else:
            return next_image()
    elif request.method == 'POST':
        if request.args.get('image') == 1:
            print('pressed on a photo')
            return increase_city_score(request)
        else:
            return update_perk(request)


votes = {}


def increase_city_score(local_request):
    city_name = request.args.get('city_key')
    votes[city_name] += 1
    return jsonify({'status': 'confirmed'})


def


def next_image():
    config = configparser.ConfigParser()
    config.read(CONFIG_FP)

    img_getter = ImageGetterCached(config['google.api']['developer_key'], config['google.api']['cx'])
    cities = {'city1_name': 'istanbul', 'city2_name': 'groningen', 'city1': '', 'city2': ''}
    imgs = img_getter.get_random_imgs("istanbul", "groningen")
    cities['city1'] = imgs[0]
    cities['city2'] = imgs[1]
    return jsonify(cities)


def remove_question(name):
    for i in range(len(questions)):
        if questions[i]['question_perk'] == name:
            questions.pop(i)
            break


def update_perk(local_request):
    global city_perks
    perk = local_request.args.get('question_perk')
    value = local_request.args.get('value')
    remove_question(perk)
    print('updating city perk ' + str(perk) + ' to ' + str(value))
    city_perks[perk] = value
    print(city_perks)
    return jsonify({'status': 'confirmed'})


def next_question():
    return jsonify(random.choice(list(questions)))


@app.route('/final', methods=['GET'])
def final_result():
    cities = ScoreCalculator(city_perks).get_city_recommendation(3)
    flights = []
    config = configparser.ConfigParser()
    config.read(CONFIG_FP)
    for city in cities:
        flights.append(PriceFinder(config['skyscanner.api']['api_key']).get_price(city, max_results=1))
    return jsonify(flights)


@app.route('/image')
def test():
    config = configparser.ConfigParser()
    config.read(CONFIG_FP)

    img_getter = ImageGetterCached(config['google.api']['developer_key'], config['google.api']['cx'])
    imgs = img_getter.get("Istanbul")
    print(imgs)


if __name__ == '__main__':
    app.run()
