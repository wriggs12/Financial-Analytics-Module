from .option_pricer import BlackScholes, MonteCarlo


class RequestHandler:
    @staticmethod
    def parse_arguments(request):
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
                raise Exception("All parameters must be provided and non-zero")
        except (TypeError, ValueError) as e:
            raise Exception(f"Invalid Input: {e}")

        return S, K, T, r, q, sigma, include_greeks, option_type

    @staticmethod
    def handle_black_scholes_calc_request(request):
        try:
            return BlackScholes.price_option(*RequestHandler.parse_arguments(request)) asfhsjgdhjklhsgdjkfghjksdfgjkgdfjksgddjkfghsj,dghfjkh
        except Exception as e:
            return f"Failed to price option: {e}"

    @staticmethod
    def handle_monte_carlo_calc_request(request):
        try:
            return MonteCarlo.price_option(*RequestHandler.parse_arguments(request))
        except Exception as e:
            return f"Failed to price option: {e}"
