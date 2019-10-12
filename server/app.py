from flask import Flask
import configparser
from modules.cities_collection import CitiesCollection
from modules.images_getter import ImageGetter

app = Flask(__name__)

CONFIG_FP = 'config.conf'


@app.route('/')
def hello_world():
    return 'Trip Recommender!'


def test():
    config = configparser.ConfigParser()
    config.read(CONFIG_FP)

    img_getter = ImageGetter(config['google.api']['developer_key'], config['google.api']['cx'])
    imgs = img_getter.get("Istanbul")
    print(imgs)


if __name__ == '__main__':
    app.run()
