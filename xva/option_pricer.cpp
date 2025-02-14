#include <iostream>
#include <stdexcept>
#include <cmath>

#include "option_pricer.h"

Option::Option(double spot, double strike, double time, double rate, double div, double vol, int type)
{
    if (type != 0 && type != 1)
        throw std::invalid_argument("Invalid Option Type!");

    _stock_price = spot;
    _strike_price = strike;
    _risk_free_rate = rate;
    _volatility = vol;
    _dividend_yield = div;
    _time_to_expiration = time;
    _option_type = type;
}

double Option::stock_price() const { return _stock_price; }
double Option::strike_price() const { return _strike_price; }
double Option::risk_free_rate() const { return _risk_free_rate; }
double Option::volatility() const { return _volatility; }
double Option::dividend_yield() const { return _dividend_yield; }
double Option::time_to_expiration() const { return _time_to_expiration; }
int Option::option_type() const { return _option_type; }

double Option::price_scholes()
{
    return BlackScholes::price_option(*this);
}

double BlackScholes::calc_d1(const Option &option)
{
    return (
        (std::log(option.stock_price() / option.strike_price()) +
         (option.risk_free_rate() - option.dividend_yield() + std::pow(option.volatility(), 2) / 2) *
             option.time_to_expiration()) /
        (option.volatility() * std::sqrt(option.time_to_expiration())));
}

double BlackScholes::calc_d2(const Option &option, double d1)
{
    return (d1 - option.volatility() * std::sqrt(option.time_to_expiration()));
}

double BlackScholes::norm_cdf(double value)
{
    return 0.5 * erfc(-value * M_SQRT1_2);
}

double BlackScholes::price_option(const Option &option)
{
    double d1 = BlackScholes::calc_d1(option);
    double d2 = BlackScholes::calc_d2(option, d1);

    double price;

    if (option.option_type() == 0)
        price = option.stock_price() *
                    std::exp(-option.dividend_yield() * option.time_to_expiration()) *
                    BlackScholes::norm_cdf(d1) -
                option.strike_price() *
                    std::exp(-option.risk_free_rate() * option.time_to_expiration()) *
                    BlackScholes::norm_cdf(d2);
    else
        price = option.strike_price() *
                    std::exp(-option.risk_free_rate() * option.time_to_expiration()) *
                    BlackScholes::norm_cdf(-d2) -
                option.stock_price() *
                    std::exp(-option.dividend_yield() * option.time_to_expiration()) *
                    BlackScholes::norm_cdf(-d1);

    return price;
}

int main()
{
    Option option(50, 52, 1.2, 0.03, 0.01, 0.2, 1);
    std::cout << option.price_scholes() << std::endl;
    return 0;
}
