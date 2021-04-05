import json

from flask import request
from flask_restful import Resource
from src import log


class Controller(Resource):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def post():
        log.info(f"Incoming request {json.dumps(json.dumps(request.json))}")
        return "OK", 200
