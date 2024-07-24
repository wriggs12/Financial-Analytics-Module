from scipy.stats import norm
import datetime
import numpy as np
import math


class BlackScholes:
    @staticmethod
    def price_option(S, K, T, r, q, sigma, include_greeks=0, type=0):
        if type not in [0, 1]:
            return

        d1 = (np.log(S / K) + (r - q + math.pow(sigma, 2) / 2) * T) / (
            sigma * np.sqrt(T)
        )
        d2 = d1 - sigma * np.sqrt(T)

        if type == 0:
            price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(
                -r * T
            ) * norm.cdf(d2)
        else:
            price = K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(
                -q * T
            ) * norm.cdf(-d1)

        if not bool(include_greeks):
            return {"Price": price}

        delta = BlackScholes.calc_delta(d1, q, T, type)
        gamma = BlackScholes.calc_gamma(d1, S, T, sigma, q)
        theta = BlackScholes.calc_theta(d1, d2, S, K, T, r, sigma, q, type)
        vega = BlackScholes.calc_vega(d1, S, T, q)
        rho = BlackScholes.calc_rho(d2, K, T, r, type)

        return {
            "Price": price,
            "Delta": delta,
            "Gamma": gamma,
            "Theta": theta,
            "Vega": vega,
            "Rho": rho,
        }

    @staticmethod
    def calc_delta(d1, q, T, type):
        if type == 0:
            return math.exp(-q * T) * norm.cdf(d1)
        return math.exp(-q * T) * -norm.cdf(-d1)

    @staticmethod
    def calc_gamma(d1, S, T, sigma, q):
        return norm.pdf(d1) * math.exp(-q * T) / (S * sigma * np.sqrt(T))

    @staticmethod
    def calc_theta(d1, d2, S, K, T, r, sigma, q, type):
        if type == 0:
            return (
                -((S * norm.pdf(d1) * sigma * math.exp(-q * T)) / (2 * np.sqrt(T)))
                - r * K * math.exp(-r * T) * norm.cdf(d2)
                + q * S * math.exp(-q * T) * norm.cdf(d1)
            )
        return (
            -((S * norm.pdf(d1) * sigma * math.exp(-q * T)) / (2 * np.sqrt(T)))
            + r * K * math.exp(-r * T) * norm.cdf(-d2)
            - q * S * math.exp(-q * T) * norm.cdf(-d1)
        )

    @staticmethod
    def calc_vega(d1, S, T, q):
        return S * math.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

    @staticmethod
    def calc_rho(d2, K, T, r, type):
        if type == 0:
            return K * T * np.exp(-r * T) * norm.cdf(d2)
        return -K * T * np.exp(-r * T) * norm.cdf(-d2)


class MonteCarlo:
    def __init__(self):
        pass

    def monte_carlo(price_data):
        def calc_trajectory(price_data):
            price_trajectory = []

            for i in range(len(price_data) - 1):
                price_trajectory.append(np.log(price_data[i] / price_data[i + 1]))

            return price_trajectory

        price_trajectory = calc_trajectory(price_data)
        risk_free_rate = np.mean(price_trajectory)
        variance = np.var(price_trajectory)
        drift = risk_free_rate - 0.5 * variance

        num_simulations = 1000
        num_steps = 100

        strike_price = 0
        stock_price = price_data[0]
        market_price = 0

        matrurity_date = datetime.date(2025, 7, 20)
        time_to_maturity = ((matrurity_date - datetime.date.today()).days + 1) / 365

        dt = time_to_maturity / num_steps

        print(price_trajectory)
        print(risk_free_rate)
        print(variance)
        print(drift)

        simulated_stock_prices = []
        for _ in range(num_simulations):
            step_stock_prices = []
            for _ in range(num_steps):
                random_input = math.sqrt(variance) * np.random.normal()
                step_price = stock_price * math.exp(drift + random_input)
                step_stock_prices.append(step_price)
            simulated_price = np.mean(step_stock_prices)
            simulated_stock_prices.append(simulated_price)
            print(simulated_stock_prices)
            break
