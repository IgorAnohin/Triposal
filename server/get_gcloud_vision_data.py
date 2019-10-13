from google.cloud import vision
import time
import pickle
import pandas as pd


def get_labels(client, url):
    time.sleep(1.5)
    try:
        resp = client.annotate_image({
            'image': {'source': {'image_uri': url}},
            'features': [{'type': vision.enums.Feature.Type.LABEL_DETECTION}],
        })

        def get_info(ann):
            return {'description': ann.description, 'score': ann.score}

        return [get_info(ann) for ann in resp.label_annotations]
    except RuntimeError as e:
        print(e)
        return []


def get_data(urls):
    client = vision.ImageAnnotatorClient()
    data = {}
    for url in urls:
        data[url] = get_labels(client, url)
    return data


def get_all_urls():
    lst = pd.read_csv("data/sightseeing.csv")['urls'].dropna()
    lst = list(map(lambda x: x.split(' '), lst))
    return [j for sub in lst for j in sub]


def dump_data(data):
    pickle.dump(data, open("data/image_labels.pickle", "wb"))


def main():
    urls = get_all_urls()
    print('urls')
    print(urls[:10])
    # data = get_data(urls)
    # dump_data(data)

main()
