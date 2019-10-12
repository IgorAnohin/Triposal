import random

from flask import Flask, jsonify, request
import configparser
from modules.cities_collection import CitiesCollection
from modules.images_getter import ImageGetterCached

app = Flask(__name__)

CONFIG_FP = 'config.conf'
app = Flask(__name__)

questions = [
    {'question_text': 'is internet speed important', 'question_perk': 'internet_speed', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'overall_safety', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'affordable_prices', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'entertainment_variety', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'air_quality', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'spacious', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'business_center', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'good_education', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'safe_roads', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'freedom_of_speech', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'democratic', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'good_english', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'safe_for_women', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'avoid_humidity', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'winter_temperature', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'summer_temperature', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'healthcare', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'lgbt_tolerance', 'min': 0, 'max': 5},
    {'question_text': 'question text', 'question_perk': 'less_smokers', 'min': 0, 'max': 5}]

city_perks = {'internet_speed': 0,
              'overall_safety': 0,
              'affordable_prices': 0,
              'entertainment_variety': 0,
              'air_quality': 0,
              'spacious': 0,
              'business_center': 0,
              'good_education': 0,
              'safe_roads': 0,
              'freedom_of_speech': 0,
              'democratic': 0,
              'good_english': 0,
              'safe_for_women': 0,
              'avoid_humidity': 0,
              'winter_temperature': 0,
              'summer_temperature': 0,
              'healthcare': 0,
              'lgbt_tolerance': 0,
              'less_smokers': 0}


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return next_question()
    elif request.method == 'POST':
        return update_perk(request)
    else:
        return jsonify({'quarks': questions})


def update_perk(request):
    perk = request.args.get('question_perk')
    value = request.args.get('value')
    questions.pop(perk)
    print(len(questions))
    city_perks[perk] = value


def next_question():
    return jsonify(random.choice(list(questions)))


@app.route('/final', methods=['GET'])
def main():
    return 'kek'


@app.route('/image')
def test():
    config = configparser.ConfigParser()
    config.read(CONFIG_FP)

    img_getter = ImageGetterCached(config['google.api']['developer_key'], config['google.api']['cx'])
    imgs = img_getter.get("Istanbul")
    print(imgs)


if __name__ == '__main__':
    app.run()
