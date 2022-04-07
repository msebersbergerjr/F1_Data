import requests, json, numpy as np


def connection(url):
    """
    Try and Establish a Connection to given website
    Return: data in json format
    """

    try:
        response = requests.get(url)

        if not response.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(response)

        geodata = response.json()
        return geodata

    except requests.exceptions.RequestException as e:
        return "Error: {}".format(e)
