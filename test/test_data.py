from woo_py.models.data import Country, Currency
from woo_py.woo import Woo


def test_data_methods(woo: Woo):
    # Test countries endpoints
    countries = woo.get_countries()
    assert len(countries) > 0
    
    # Test getting a specific country (using US as an example)
    us = woo.get_country("US")
    assert us is not None
    assert us.code == "US"
    assert us.name is not None
    
    # Test currencies endpoints
    currencies = woo.get_currencies()
    assert len(currencies) > 0
    
    # Test getting a specific currency (using USD as an example)
    usd = woo.get_currency("USD")
    assert usd is not None
    assert usd.code == "USD"
    assert usd.name is not None
    assert usd.symbol is not None