import pytest

from modules.option_pricer import BlackScholes

STOCK_PRICE = 10.24
STRIKE_PRICE = 10.27
TIME_TO_EXPIRATION = 0.34
RISK_FREE_RATE = 0.01
DIVIDEND_YIELD = 0.03
VOLATILITY = 0.45


def test_call_pricing():
    pricing_response = BlackScholes.price_option(
        STOCK_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRATION,
        RISK_FREE_RATE,
        DIVIDEND_YIELD,
        VOLATILITY,
        0,
        0,
    )

    assert pricing_response.get("Price") == pytest.approx(1.01437, 0.001)
    assert pricing_response.get("Delta") is None
    assert pricing_response.get("Gamma") is None
    assert pricing_response.get("Theta") is None
    assert pricing_response.get("Vega") is None
    assert pricing_response.get("Rho") is None


def test_call_greeks():
    pricing_response = BlackScholes.price_option(
        STOCK_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRATION,
        RISK_FREE_RATE,
        DIVIDEND_YIELD,
        VOLATILITY,
        1,
        0,
    )

    assert pricing_response.get("Price") == pytest.approx(1.01437, 0.001)
    assert pricing_response.get("Delta") == pytest.approx(0.53204, 0.001)
    assert pricing_response.get("Gamma") == pytest.approx(0.14632, 0.001)
    assert pricing_response.get("Theta") == pytest.approx(-1.43435, 0.001)
    assert pricing_response.get("Vega") == pytest.approx(2.34744, 0.001)
    assert pricing_response.get("Rho") == pytest.approx(1.50747, 0.001)


def test_put_pricing():
    pricing_response = BlackScholes.price_option(
        STOCK_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRATION,
        RISK_FREE_RATE,
        DIVIDEND_YIELD,
        VOLATILITY,
        0,
        1,
    )

    assert pricing_response.get("Price") == pytest.approx(1.11343, 0.001)
    assert pricing_response.get("Delta") is None
    assert pricing_response.get("Gamma") is None
    assert pricing_response.get("Theta") is None
    assert pricing_response.get("Vega") is None
    assert pricing_response.get("Rho") is None


def test_put_greeks():
    pricing_response = BlackScholes.price_option(
        STOCK_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRATION,
        RISK_FREE_RATE,
        DIVIDEND_YIELD,
        VOLATILITY,
        1,
        1,
    )

    assert pricing_response.get("Price") == pytest.approx(1.11343, 0.001)
    assert pricing_response.get("Delta") == pytest.approx(-0.45780, 0.001)
    assert pricing_response.get("Gamma") == pytest.approx(0.14632, 0.001)
    assert pricing_response.get("Theta") == pytest.approx(-1.63608, 0.001)
    assert pricing_response.get("Vega") == pytest.approx(2.34744, 0.001)
    assert pricing_response.get("Rho") == pytest.approx(-1.97247, 0.001)
