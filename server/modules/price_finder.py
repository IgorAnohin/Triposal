# System Dependencies
import os
import requests
import datetime

# Config
api_key = os.environ.get("api_key", "")
if not api_key:
    print("No api key found")
    exit()


def get_place_info(city_name, from_country_id="ES"):
    url = f"https://www.skyscanner.net/g/chiron/api/v1/places/autosuggest/v1.0/{from_country_id}/EUR/en-US/"

    querystring = {"query": city_name}

    payload = ""
    headers = {
        'Accept': "application/json",
        'api-key': api_key
    }

    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring)

    if (response.ok):
        data = response.json()["Places"][0]
        print("price_finder:get_place_info: Got city name",
              data.get("PlaceName", "NONE"))
        return data
    print("ERROR:price_finder:get_place_info: No place found for query", city_name)
    return None


def get_price(to_city_name, from_city_id="BCN-sky", from_country_id="ES", outbound_date="2019-11", inbound_date="2019-11", max_results=10):
    to_city_data = get_place_info(to_city_name)
    if not (to_city_data) or not to_city_data.get("PlaceId", ""):
        print("ERROR:price_finder:get_price: No city info found")
        return None
    to_city_id = to_city_data.get("PlaceId")

    url = f"https://www.skyscanner.net/g/chiron/api/v1/flights/browse/browsequotes/v1.0/{from_country_id}/EUR/en-US/{from_city_id}/{to_city_id}/{outbound_date}/{inbound_date}"
    payload = ""
    headers = {
        'Accept': "application/json",
        'api-key': api_key
    }

    response = requests.request(
        "GET", url, data=payload, headers=headers)

    if (response.ok):
        data = response.json().get("Quotes", [])
        to_return = sorted(data, key=lambda x: x.get("MinPrice","QuoteDateTime"))
        return to_return[:min([max_results,len(to_return)])]
    print("ERROR:price_finder:get_price: No flights found")
    return None

print(get_price("Duba")[0])