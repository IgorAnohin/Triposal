import requests
import datetime


def get_last_week():
    today = datetime.datetime.now()
    next_week = (today + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    next_week2 = (today + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
    return next_week, next_week2


class PriceFinder:
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key:
            print("No api key found")

    def _get_place_info(self, city_name, from_country_id="ES"):
        url = f"https://www.skyscanner.net/g/chiron/api/v1/places/autosuggest/v1.0/{from_country_id}/EUR/en-US/"
        querystring = {"query": city_name}
        payload = ""
        headers = {
            'Accept': "application/json",
            'api-key': self.api_key
        }
        response = requests.request(
            "GET", url, data=payload, headers=headers, params=querystring)

        if response.ok and len(response.json()['Places']) > 0:
            data = response.json()['Places'][0]
            print("price_finder:get_place_info: Got city name",
                  data.get('PlaceName', 'NONE'))
            return data
        print("ERROR:price_finder:get_place_info: No place found for query", city_name)
        return None

    def get_price(self, to_city_name, from_city_id="BCN-sky", from_country_id="ES", max_results=10):
        outbound_date, inbound_date = get_last_week()

        to_city_data = self._get_place_info(to_city_name)
        if not to_city_data or not to_city_data.get("PlaceId", ""):
            print("ERROR:price_finder:get_price: No city info found")
            return None
        to_city_id = to_city_data.get("PlaceId")

        url = f"https://www.skyscanner.net/g/chiron/api/v1/flights/browse/browsequotes/v1.0/{from_country_id}/EUR/en-US/{from_city_id}/{to_city_id}/{outbound_date}/{inbound_date}"
        payload = ""
        headers = {
            'Accept': "application/json",
            'api-key': self.api_key
        }

        response = requests.request(
            "GET", url, data=payload, headers=headers)

        if response.ok:
            data = response.json().get("Quotes", [])
            to_return = sorted(data, key=lambda x: x.get("MinPrice", "QuoteDateTime"))
            return to_return[:min([max_results, len(to_return)])]
        print("ERROR:price_finder:get_price: No flights found")
        return None
