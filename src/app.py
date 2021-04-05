from flask import Flask
from flask_restful import Api

from src.solver.api.controller import Controller


def create_app():
    _app = Flask(__name__)
    api = Api(_app)
    api.add_resource(Controller, '/')
    return _app


app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False, port=5000)
