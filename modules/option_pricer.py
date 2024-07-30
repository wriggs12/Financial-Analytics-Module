from scipy.stats import norm
from numpy.random import randn
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
    def monte_carlo(S, K, T, r, q, sigma, steps, N):
        n = 10_000_000
        p = 0.5
        r1, r2, r3 = 0.2, 0.8, 0.4
        s1, s2, s3 = 0.1, 0.05, 0.2

        X_1 = np.exp(r1 + s1 * randn())
        X_2 = np.exp(r2 + s2 * randn())
        X_3 = np.exp(r3 + s3 * randn())

        S = (X_1 + X_2 + X_3) ** p

        print(S.mean())

        st = np.cumsum(np.random.normal(size=(100, 1000)), axis=0)
        plt.plot(np.exp(st))
        plt.xlabel("Time Increments")
        plt.ylabel("Stock Price")
        plt.title("Geometric Brownian Motion")


if __name__ == "__main__":
    monte_carlo = MonteCarlo()
    monte_carlo.monte_carlo(0, 0, 0, 0, 0, 0, 0, 0)
