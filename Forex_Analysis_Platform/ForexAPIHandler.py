import requests

# Might be useful to have a list of constants corresponding to currencies as strings
URL_BASE = 'https://www.freeforexapi.com/api/live'

def get_all_currency_pairs():
    response = requests.get(URL_BASE)
    currency_pairs = response.json()
    return currency_pairs['supportedPairs']

def get_currency_rate(currency_pair):
    url = "{}?pairs={}".format(URL_BASE, currency_pair)
    response = requests.get(url)
    currency_rate = response.json()['rates'][currency_pair]['rate']
    return currency_rate

#print(get_all_currency_pairs());

print(get_currency_rate('USDAUD'))
