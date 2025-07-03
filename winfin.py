import os

from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from modules.request_handler import RequestHandler

FRONTEND_ORIGIN = "https://winstonriggs.com"

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per minute"])
CORS(app, resources={r"/*": {"origins": FRONTEND_ORIGIN}})

@app.route("/blackScholesPricing", methods=["GET"])
@limiter.limit("10 per minute")
def handle_black_scholes_request():
    params = request.args.to_dict()
    return RequestHandler.handle_black_scholes_calc_request(params)


@app.route("/monteCarloPricing", methods=["GET"])
@limiter.limit("5 per minute")
def handle_monte_carlo_request():
    params = request.args.to_dict()
    return RequestHandler.handle_monte_carlo_calc_request(params)


@app.route("/fetchEquityData", methods=["GET"])
@limiter.limit("20 per minute")
def handle_equity_data_request():
    params = request.args.to_dict()
    return RequestHandler.handle_equity_data_request(params)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
