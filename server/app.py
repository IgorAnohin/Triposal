from flask import Flask
from modules.cities_collection import CitiesCollection
from modules.images_getter import ImageGetter

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Trip Recommender!'


def main():
    tmp = CitiesCollection()
    print(tmp.data)


if __name__ == '__main__':
    # app.run()
    main()
