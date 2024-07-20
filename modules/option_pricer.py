import numpy as np
import datetime
import math

def black_scholes():
    pass

def monte_carlo(price_data):
    def calc_trajectory(price_data):
        price_trajectory = []
        
        for i in range(len(price_data) - 1):
            price_trajectory.append(np.log(price_data[i] / price_data[i+1]))
        
        return price_trajectory

    price_trajectory = calc_trajectory(price_data)
    risk_free_rate = np.mean(price_trajectory)
    variance = np.var(price_trajectory)
    drift = risk_free_rate - 0.5*variance

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


if __name__ == '__main__':
    monte_carlo([9, 7, 8, 4, 6, 5, 3])