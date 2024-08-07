from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import math


# Formulas defined here: https://www.columbia.edu/~mh2078/FoundationsFE/BlackScholes.pdf
class BlackScholes:
    @staticmethod
    def price_option(S, K, T, r, q, sigma, include_greeks=0, type=0):
        if type not in [0, 1]:
            raise Exception("Invalid Option Type")

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
    @staticmethod
    def price_option(S, K, T, r, q, sigma, include_greeks=0, type=0):
        price = MonteCarlo.monte_carlo(S, K, T, r, q, sigma, type)

        if not bool(include_greeks):
            return {"Price": price}

        delta, gamma = MonteCarlo.calc_delta_gamma(S, K, T, r, q, sigma, price, type)
        theta = MonteCarlo.calc_theta(S, K, T, r, q, sigma, price, type)
        vega = MonteCarlo.calc_vega(S, K, T, r, q, sigma, price, type)
        rho = MonteCarlo.calc_rho(S, K, T, r, q, sigma, price, type)

        return {
            "Price": price,
            "Delta": delta,
            "Gamma": gamma,
            "Theta": theta,
            "Vega": vega,
            "Rho": rho,
        }

    @staticmethod
    def monte_carlo(
        S, K, T, r, q, sigma, type=0, num_simulations=100000, num_steps=252
    ):
        dt = T / num_steps
        nudt = (r - q - 0.5 * sigma**2) * dt
        sigsdt = sigma * np.sqrt(dt)

        Z = np.random.normal(0, 1, (num_simulations, num_steps))
        S_T = S * np.exp(np.cumsum(nudt + sigsdt * Z, axis=1))

        if type == 0:
            payoffs = np.maximum(S_T[:, -1] - K, 0)
        else:
            payoffs = np.maximum(K - S_T[:, -1], 0)

        return np.exp(-r * T) * np.mean(payoffs)

    @staticmethod
    def calc_delta_gamma(S, K, T, r, q, sigma, price, type):
        delta_S = 0.01 * S

        price_up = MonteCarlo.monte_carlo(S + delta_S, K, T, r, q, sigma, type)
        price_down = MonteCarlo.monte_carlo(S - delta_S, K, T, r, q, sigma, type)

        delta = (price_up - price_down) / (2 * delta_S)
        gamma = (price_up + price_down - 2 * price) / (delta_S**2)

        return delta, gamma

    @staticmethod
    def calc_theta(S, K, T, r, q, sigma, price, type):
        delta_T = 1 / 365
        price_T_down = MonteCarlo.monte_carlo(S, K, T - delta_T, r, q, sigma, type)
        return (price_T_down - price) / delta_T

    @staticmethod
    def calc_vega(S, K, T, r, q, sigma, price, type):
        delta_sigma = 0.01
        price_vol_up = MonteCarlo.monte_carlo(S, K, T, r, q, sigma + delta_sigma, type)
        return (price_vol_up - price) / delta_sigma

    @staticmethod
    def calc_rho(S, K, T, r, q, sigma, price, type):
        delta_r = 0.01
        price_r_up = MonteCarlo.monte_carlo(S, K, T, r + delta_r, q, sigma, type)
        return (price_r_up - price) / delta_r


if __name__ == "__main__":
    monte_carlo = MonteCarlo()
    print(monte_carlo.price_option(100, 100, 1, 0.05, 0.02, 0.2, 1, 0))

    black_scholes = BlackScholes()
    print(black_scholes.price_option(100, 100, 1, 0.05, 0.02, 0.2, 1, 0))
