from modules.option_pricer import MonteCarlo
import pytest

STOCK_PRICE = 10.24
STRIKE_PRICE = 10.27
TIME_TO_EXPIRATION = 0.34
RISK_FREE_RATE = 0.01
DIVIDEND_YIELD = 0.03
VOLATILITY = 0.45


def test_call_pricing():
    pricing_response = MonteCarlo.price_option(
        STOCK_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRATION,
        RISK_FREE_RATE,
        DIVIDEND_YIELD,
        VOLATILITY,
        0,
        0,
    )

    assert pricing_response.get("Price") == pytest.approx(1.01437, 0.1)
    assert pricing_response.get("Delta") is None
    assert pricing_response.get("Gamma") is None
    assert pricing_response.get("Theta") is None
    assert pricing_response.get("Vega") is None
    assert pricing_response.get("Rho") is None


def test_put_pricing():
    pricing_response = MonteCarlo.price_option(
        STOCK_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRATION,
        RISK_FREE_RATE,
        DIVIDEND_YIELD,
        VOLATILITY,
        0,
        1,
    )

    assert pricing_response.get("Price") == pytest.approx(1.11343, 0.1)
    assert pricing_response.get("Delta") is None
    assert pricing_response.get("Gamma") is None
    assert pricing_response.get("Theta") is None
    assert pricing_response.get("Vega") is None
    assert pricing_response.get("Rho") is None
