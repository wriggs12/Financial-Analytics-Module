#ifndef OPTION_PRICER_H
#define OPTION_PRICE_H

class Option
{
public:
    enum OptionType
    {
        PUT = 0,
        CALL = 1
    };

private:
    double _stock_price;
    double _strike_price;
    double _risk_free_rate;
    double _volatility;
    double _dividend_yield;
    double _time_to_expiration;
    OptionType _option_type;

public:
    Option(double spot, double strike, double rate, double vol, double div, double time, OptionType type);

    double stock_price() const;
    double strike_price() const;
    double risk_free_rate() const;
    double volatility() const;
    double dividend_yield() const;
    double time_to_expiration() const;
    OptionType option_type() const;

    double price_scholes();
};

class BlackScholes
{
private:
    static double calc_d1(const Option &option);
    static double calc_d2(const Option &option, double d1);
    static double norm_cdf(double value);

public:
    static double price_option(const Option &option);
};

#endif
