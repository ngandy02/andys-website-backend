from flask import Flask, request
from flask_restx import Resource, Api 
from flask_cors import CORS

import werkzeug.exceptions as wz
import data.submission as sub

SUBMISSIONS_EP = "/submissions"
MESSAGE = "message"
RETURN = "return"

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route('/')
class Hello(Resource):
    def home(self):
        return "Hello World"


@api.route(f'{SUBMISSIONS_EP}/create')
class Submit(Resource):
    """
    Create a new feedback submission.
    """
    def put(self):
        if not request.json:
            raise wz.BadRequest("JSON body required")
        name = request.json.get(sub.NAME)
        email = request.json.get(sub.EMAIL)
        feedback = request.json.get(sub.FEEDBACK)
        if not email or not name or not feedback:
            raise wz.BadRequest("Name, email, and feedback are required to complete this form!")
        try:
            # returns the users email
            ret = sub.submit(name, email, feedback)
            return {
                MESSAGE: "Feedback Submitted!",
                RETURN: ret
            }
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')
       

@api.route(SUBMISSIONS_EP)
class Submissions(Resource):
    """
    Read or extract all of the submitted feedbacks
    """
    def get(self):
       return sub.read_submissions()
    

@api.route(f'{SUBMISSIONS_EP}/<email>')
class SubmissionsFromOneEmail(Resource):
    """
    Read of extract all submitted entries from one email or person
    """
    def get(self, email):
        return sub.get_submission(email)


if __name__ == "__main__":
    app.run(debug=True)