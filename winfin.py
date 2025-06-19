import os

from flask import Flask, request
from flask_cors import CORS

from modules.request_handler import RequestHandler

app = Flask(__name__)
CORS(app)


@app.route("/blackScholesPricing", methods=["GET"])
def handle_black_scholes_request():
    params = request.args.to_dict()
    return RequestHandler.handle_black_scholes_calc_request(params)


@app.route("/monteCarloPricing", methods=["GET"])
def handle_monte_carlo_request():
    params = request.args.to_dict()
    return RequestHandler.handle_monte_carlo_calc_request(params)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
