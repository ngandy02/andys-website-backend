from flask import Flask, request
from flask_restx import Resource, Api 
from flask_cors import CORS

import werkzeug.exceptions as wz
import data.submission as sub

SUBMIT_EP = "/submit"

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route('/')
def home():
    return "Hello World"


@api.route(SUBMIT_EP)
class Register(Resource):
    def put(self):
        if not request.json:
            raise wz.BadRequest("JSON body required")
        name = request.json.get(sub.NAME)
        email = request.json.get(sub.EMAIL)
        if not email or not name:
            raise wz.BadRequest("Both name and email are required")
        try:
            sub.register(name, email)
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')
        return {"email": email}


if __name__ == "__main__":
    app.run(debug=True)