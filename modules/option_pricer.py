import math
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


class OptionType(Enum):
    PUT = 0
    CALL = 1


def bisection(f, a, b, tol=0.1, maxiter=10):
    n = 0
    while n < maxiter:
        c = (a + b) * 0.5
        if f(c) == 0 or abs(a - b) * 0.5 < tol:
            return c, n

        n += 1
        if f(c) < 0:
            a = c
        else:
            b = c

    return c, n


# Formulas defined here: http://naneport.arg.in.th/books/ComputerIT/Mastering%20Python%20for%20Finance.pdf
class StockOption:
    def __init__(
        self,
        S: float,
        K: float,
        T: float = 1,
        N: float = 2,
        r: float = 0.05,
        q: float = 0.0,
        pu: float = 0.0,
        pd: float = 0.0,
        sigma: float = 0.0,
        option_type: OptionType = OptionType.CALL,
        is_european: bool = False,
    ):
        """
        :param S: initial stock price
        :param K: strike price
        :param T: time to maturity
        :param N: number of time steps
        :param r: risk-free rate
        :param q: dividend yield
        :param pu: probability at up state
        :param pd: probability at down state
        :param sigma: volatility
        :param type: option type
        """

        self.S = S
        self.K = K
        self.T = T
        self.N = N
        self.r = r
        self.q = q
        self.pu = pu
        self.pd = pd
        self.sigma = sigma
        self.option_type = option_type
        self.is_european = is_european

    @property
    def dt(self):
        return self.T / self.N

    @property
    def df(self):
        return math.exp(-(self.r - self.q) * self.dt)


class BinomialTreeOption(StockOption):
    def init_params(self):
        self.u = 1 + self.pu
        self.d = 1 - self.pd
        self.qu = (math.exp((self.r - self.q) * self.dt) - self.d) / (self.u - self.d)
        self.qd = 1 - self.qu

    def init_stock_price_tree(self):
        self.STs = [np.array([self.S])]

        for _ in range(self.N):
            prev_branches = self.STs[-1]
            st = np.concatenate((prev_branches * self.u, [prev_branches[-1] * self.d]))
            self.STs.append(st)

    def init_payoffs_tree(self):
        if self.option_type is OptionType.CALL:
            return np.maximum(0, self.STs[self.N] - self.K)
        else:
            return np.maximum(0, self.K - self.STs[self.N])

    def check_early_exercise(self, payoffs, node):
        if self.option_type is OptionType.CALL:
            return np.maximum(payoffs, self.STs[node] - self.K)
        else:
            return np.maximum(payoffs, self.K - self.STs[node])

    def traverse_tree(self, payoffs):
        for i in reversed(range(self.N)):
            payoffs = (payoffs[:-1] * self.qu + payoffs[1:] * self.qd) * self.df

            if not self.is_european:
                payoffs = self.check_early_exercise(payoffs, i)

        return payoffs

    def price(self):
        self.init_params()
        self.init_stock_price_tree()
        payoffs = self.traverse_tree(self.init_payoffs_tree())
        return payoffs[0]


class BinomialLROption(BinomialTreeOption):
    def init_params(self):
        odd_N = self.N if (self.N % 2 == 0) else (self.N + 1)
        d1 = (
            math.log(self.S / self.K)
            + ((self.r - self.q) + (self.sigma**2) / 2) * self.T
        ) / (self.sigma * math.sqrt(self.T))
        d2 = (
            math.log(self.S / self.K)
            + ((self.r - self.q) - (self.sigma**2) / 2) * self.T
        ) / (self.sigma * math.sqrt(self.T))

        pbar = self.pp_2_inversion(d1, odd_N)
        self.p = self.pp_2_inversion(d2, odd_N)
        self.u = 1 / self.df * pbar / self.p
        self.d = (1 / self.df - self.p * self.u) / (1 - self.p)
        self.qu = self.p
        self.qd = 1 - self.p

    def pp_2_inversion(self, z, n):
        return 0.5 + math.copysign(1, z) * math.sqrt(
            0.25
            - 0.25
            * math.exp(
                -((z / (n + 1.0 / 3.0 + 0.1 / (n + 1.0))) ** 2.0) * (n + 1.0 / 6.0)
            )
        )


class ImpliedVolatilityModel:
    def __init__(self, S, r=0.05, T=1, q=0, N=1, option_type=OptionType.CALL):
        self.S = S
        self.r = r
        self.T = T
        self.q = q
        self.N = N
        self.option_type = option_type

    def option_valuation(self, K, sigma):
        lr_option = BinomialLROption(
            S=self.S,
            K=K,
            T=self.T,
            N=self.N,
            r=self.r,
            option_type=self.option_type,
            sigma=sigma,
        )
        return lr_option.price()

    def get_implied_volatilities(self, strikes, opt_price):
        imp_vols = []

        for i, strike in enumerate(strikes):
            f = lambda sigma: self.option_valuation(strike, sigma) - opt_price[i]
            imp_vol = bisection(f, 0.01, 0.99, 0.0001, 100)[0]
            imp_vols.append(imp_vol)

        return imp_vols


# Formulas defined here: https://www.columbia.edu/~mh2078/FoundationsFE/BlackScholes.pdf
class BlackScholes:
    @staticmethod
    def price_option(S, K, T, r, q, sigma, include_greeks=0, type=0):
        if type not in [0, 1]:
            raise Exception("Invalid Option Type: Must be 0 (put) or 1 (call)")

        sqrt_T = np.sqrt(T)
        exp_neg_qT = math.exp(-q * T)
        exp_neg_rT = math.exp(-r * T)

        d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
        d2 = d1 - sigma * sqrt_T

        if type == 0:
            price = S * exp_neg_qT * norm.cdf(d1) - K * exp_neg_rT * norm.cdf(d2)
        else:
            price = K * exp_neg_rT * norm.cdf(-d2) - S * exp_neg_qT * norm.cdf(-d1)

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
