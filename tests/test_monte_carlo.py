from unittest.mock import patch

import numpy as np

from modules.option_pricer import MonteCarlo

STOCK_PRICE = 10.24
STRIKE_PRICE = 10.27
TIME_TO_EXPIRATION = 0.34
RISK_FREE_RATE = 0.01
DIVIDEND_YIELD = 0.03
VOLATILITY = 0.45


@patch("modules.option_pricer.np.random.normal")
def test_call_pricing(mock_normal):
    rng = np.random.default_rng(seed=42)
    mock_normal.return_value = rng.normal(0, 1, (100000, 252))

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

    assert pricing_response.get("Price") == 1.0185873270635142
    assert pricing_response.get("Delta") is None
    assert pricing_response.get("Gamma") is None
    assert pricing_response.get("Theta") is None
    assert pricing_response.get("Vega") is None
    assert pricing_response.get("Rho") is None


@patch("modules.option_pricer.np.random.normal")
def test_call_greeks(mock_normal):
    rng = np.random.default_rng(seed=42)
    mock_normal.return_value = rng.normal(0, 1, (100000, 252))

    pricing_response = MonteCarlo.price_option(
        STOCK_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRATION,
        RISK_FREE_RATE,
        DIVIDEND_YIELD,
        VOLATILITY,
        1,
        0,
    )

    assert pricing_response.get("Price") == 1.0185873270635142
    assert pricing_response.get("Delta") == 0.5318108065618921
    assert pricing_response.get("Gamma") == 0.15422651642233928
    assert pricing_response.get("Theta") == -1.4479696296132694
    assert pricing_response.get("Vega") == 2.362925859403897
    assert pricing_response.get("Rho") == 1.5119835994692021


@patch("modules.option_pricer.np.random.normal")
def test_put_pricing(mock_normal):
    rng = np.random.default_rng(seed=42)
    mock_normal.return_value = rng.normal(0, 1, (100000, 252))

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

    assert pricing_response.get("Price") == 1.1120268739317472
    assert pricing_response.get("Delta") is None
    assert pricing_response.get("Gamma") is None
    assert pricing_response.get("Theta") is None
    assert pricing_response.get("Vega") is None
    assert pricing_response.get("Rho") is None


@patch("modules.option_pricer.np.random.normal")
def test_put_greeks(mock_normal):
    rng = np.random.default_rng(seed=42)
    mock_normal.return_value = rng.normal(0, 1, (100000, 252))

    pricing_response = MonteCarlo.price_option(
        STOCK_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRATION,
        RISK_FREE_RATE,
        DIVIDEND_YIELD,
        VOLATILITY,
        1,
        1,
    )

    assert pricing_response.get("Price") == 1.1120268739317472
    assert pricing_response.get("Delta") == -0.45858975462106777
    assert pricing_response.get("Gamma") == 0.15422651642229693
    assert pricing_response.get("Theta") == -1.6380401997228766
    assert pricing_response.get("Vega") == 2.3448934636999486
    assert pricing_response.get("Rho") == -1.9620552276178094
