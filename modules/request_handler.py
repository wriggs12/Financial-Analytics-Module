from .option_pricer import BlackScholes


class RequestHandler:
    @staticmethod
    def handle_black_scholes_calc_request(request):
        try:
            S = float(request.get("stock_price"))
            K = float(request.get("strike_price"))
            T = float(request.get("time_to_expiration"))
            r = float(request.get("risk_free_rate"))
            q = float(request.get("dividend_yield"))
            sigma = float(request.get("volatility"))
            include_greeks = int(request.get("include_greeks"))
            option_type = int(request.get("option_type"))

            if not S or not K or not T or not r or not q or not sigma:
                raise Exception("Missing Parameters")

            return BlackScholes.price_option(
                S, K, T, r, q, sigma, include_greeks, option_type
            )
        except Exception as e:
            return f"Failed to price option: {e}"
