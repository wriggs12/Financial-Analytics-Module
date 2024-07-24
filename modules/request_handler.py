from .option_pricer import BlackScholes


class RequestHandler:
    @staticmethod
    def handle_black_scholes_calc_request(request):
        try:
            S = request.get("stock_price")
            K = request.get("strike_price")
            T = request.get("time_to_expiration")
            r = request.get("risk_free_rate")
            q = request.get("dividend_yield")
            sigma = request.get("volatility")
            include_greeks = request.get("include_greeks")
            option_type = request.get("option_type")

            if not S or not K or not T or not r or not q or not sigma:
                raise Exception("Missing Parameters")

            return BlackScholes.price_option(
                S, K, T, r, q, sigma, include_greeks, option_type
            )
        except Exception as e:
            return f"Failed to price option with error: {repr(e)}"
