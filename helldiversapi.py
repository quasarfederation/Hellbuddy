import requests

"""HelldiversAPI is a wrapper that handles information from the Training Manual API. Ideally it should abstract away anything related to the api, and return the desired info."""
class HelldiversAPI:
    api_link = "https://helldiverstrainingmanual.com/api/v1/"

    @classmethod
    def get_dispatch(cls, time=41000001):
        dispatch_params = {"from": time}
        response = requests.get(f"{cls.api_link}war/news", params=dispatch_params)
        dispatch = []

        if response.ok:
            news_feed = response.json()
            dispatch = map(lambda l: HelldiversAPI._clean_json("\n", l, "message"), news_feed)
        else:
            print(f"Could not retrieve data. Error Code: {response.status_code}")

        return list(dispatch)

    @classmethod
    def get_major_order(cls):
        response = requests.get(f"{cls.api_link}war/major-orders")
        major_order_data = []

        if response.ok:
            major_order = (response.json()[0]["setting"])
            major_order_data.append(major_order["overrideTitle"])
            major_order_data.append(major_order["overrideBrief"])
            major_order_data.append(major_order["taskDescription"])
        else:
            print(f"Could not retrieve data. Error Code: {response.status_code}")

        return major_order_data

    @classmethod
    def get_campaign_info(cls):
        response = requests.get(f"{cls.api_link}war/campaign")
        planet_data = []

        if response.ok:
            for planet in response.json():
                planet_data.append(planet)
        else:
            print(f"Could not retrieve data. Error Code: {response.status_code}")

        return planet_data

    # TODO: wHAT THE FUCK IS WRONG WITH THIS???????????
    @classmethod
    def get_planet_info(cls, planet_name):
        response = requests.get(f"{cls.api_link}planets")
        planet_info = []

        if response.ok:
            planet_list = response.json()
            for planet in planet_list:
                if planet_list[planet]["name"] == planet_name:
                    planet_info = planet_list[planet]
                    break
        else:
            print(f"Could not retrieve data. Error Code: {response.status_code}")

        if not planet_info:
            print(f"Could not find planet from name: {planet_name}")
            return planet_info
        else:
            return planet_info

    # Probably a better way to do this, but this should work reliably whereas just using .find() wouldn't work.
    @staticmethod
    def _clean_json(test_char, json, category):
        start_index = 0
        for index, char in enumerate(json[category]):
            if char == test_char:
                start_index = index
        return json[category][start_index:len(json[category])]