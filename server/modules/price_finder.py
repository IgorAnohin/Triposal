import requests
import datetime


def get_last_week(fmt='%Y-%m-%d'):
    today = datetime.datetime.now()
    next_week = (today + datetime.timedelta(days=7)).strftime(fmt)
    next_week2 = (today + datetime.timedelta(days=14)).strftime(fmt)
    return next_week, next_week2


def get_booking_url(to_city_id, quote, from_city_id="BCN"):
    base_url = "https://www.skyscanner.de/transporte/vuelos/"
    outbound_date = quote.get("OutboundLeg", {}).get("DepartureDate", "")
    inbound_date = quote.get("InboundLeg", {}).get("DepartureDate", "")
    return f"{base_url}/{from_city_id}/{to_city_id}/{outbound_date}/{inbound_date}/"


class PriceFinder:
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key:
            print("No api key found")

    def get_place_info(self, city_name, from_country_id="ES"):
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

        to_city_data = self.get_place_info(to_city_name)
        if not to_city_data or not to_city_data.get("PlaceId", ""):
            print("Unable to find city. Trying with first word")
            to_city_data = self.get_place_info(to_city_name.split(" ")[0])
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
            to_return = list(map(lambda quote: {
                             **quote, 'booking_url': get_booking_url(to_city_id, quote)}, data))
            to_return = sorted(to_return, key=lambda x: x.get(
                "MinPrice", "QuoteDateTime"))
            if len(to_return) < 1:
                return [{'MinPrice': 0, 'booking_url': ''}]
            return to_return[:min([max_results, len(to_return)])]
        return [{'MinPrice': 0, 'booking_url': ''}]
