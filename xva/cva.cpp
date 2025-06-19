#include <vector>
#include <iostream>

// Σ (Cash Flow_t * Discount Factor_t)
double calc_present_value(const std::vector<double> &cash_flows, const std::vector<double> &discount_factors)
{
    double present_value = 0.0;

    for (size_t i = 0; i < cash_flows.size(); ++i)
    {
        present_value += cash_flows[i] * discount_factors[i];
    }

    return present_value;
}

// CVA = -LGD * ∑ (EE(t) * PD(t-1, t))
double calc_cva(const std::vector<double> &exposures, const std::vector<double> &probabilities, double lgd)
{
    double cva = 0.0;

    for (size_t i = 0; i < exposures.size(); ++i)
    {
        cva += exposures[i] * probabilities[i];
    }

    return cva * -lgd;
}

int main()
{
    // Hard Code Values
    double notional = 10000;
    double fixed_rate = 0.03;
    double lgd = 0.6;
    std::vector<double> floating_rates = {0.025, 0.027, 0.028};
    std::vector<double> discount_factors = {0.98, 0.95, 0.92};
    std::vector<double> probabilities = {0.01, 0.015, 0.02};

    // Cash flows for fixed leg
    std::vector<double> fixed_cash_flows;
    for (size_t i = 0; i < discount_factors.size(); ++i)
    {
        fixed_cash_flows.emplace_back(notional * fixed_rate);
    }

    // Cash flows for floating leg
    std::vector<double> floating_cash_flows;
    for (size_t i = 0; i < floating_rates.size(); ++i)
    {
        floating_cash_flows.emplace_back(notional * floating_rates[i]);
    }

    // Calculate present value of each leg
    double fixed_leg_pv = calc_present_value(fixed_cash_flows, discount_factors);
    double floating_leg_pv = calc_present_value(floating_cash_flows, discount_factors);

    // Calculate MTM value
    double mtm = floating_leg_pv - fixed_leg_pv;

    std::vector<double> exposures(discount_factors.size(), mtm / discount_factors.size());
    double cva = calc_cva(exposures, probabilities, lgd);

    std::cout << "Fixed Leg Present Value: " << fixed_leg_pv << std::endl;
    std::cout << "Floating Leg Present Value: " << floating_leg_pv << std::endl;
    std::cout << "MTM Value of Interest Rate Swap: " << mtm << std::endl;
    std::cout << "CVA: " << cva << std::endl;

    std::cout << "Exposures: ";
    for (const auto &e : exposures)
        std::cout << e << " ";
    std::cout << std::endl;

    return 0;
}
