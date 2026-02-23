from flask import Flask, request
from flask_restx import Resource, Api 
from flask_cors import CORS

import werkzeug.exceptions as wz
import data.accounts as acc

REGISTER_EP = "/register"

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route('/')
def home():
    return "Hello World"

@api.route(REGISTER_EP)
class Register(Resource):
    def put(self):
        if not request.json:
            raise wz.BadRequest("JSON body required")
        name = request.json.get(acc.NAME)
        email = request.json.get(acc.EMAIL)
        if not email or not name:
            raise wz.BadRequest("Both name and email are required")
        try:
            acc.register(name, email)
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')
        return {"email": email}




if __name__ == "__main__":
    app.run(debug=True)