from flask import Flask
from flask import request
from modules.request_handler import RequestHandler

app = Flask(__name__)


@app.route("/blackScholesPricing", methods=["GET"])
def handle_black_scholes_request():
    params = request.get_json()
    return RequestHandler.handle_black_scholes_calc_request(params)


if __name__ == "__main__":
    app.run()
