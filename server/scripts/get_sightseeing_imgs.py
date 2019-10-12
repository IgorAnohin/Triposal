import configparser
from ..modules.images_getter import ImageGetter


CONFIG_FP = 'config.conf'


def get_sightseing_urls(img_getter, country):
    return img_getter.get(country)


def grab_imgs(img_getter, countries):
    for country in countries:
        urls = get_sightseing_urls(img_getter, country)



def main():
    config = configparser.ConfigParser()
    config.read(CONFIG_FP)

    img_getter = ImageGetter(config['google.api']['developer_key'], config['google.api']['cx'])
    imgs = img_getter.get("Istanbul")


if __name__ == '__main__':
    main()
