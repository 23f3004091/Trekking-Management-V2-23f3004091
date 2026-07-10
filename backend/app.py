from flask import Flask, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources = {r'/api/': {"origins" : "http://localhost:5173"}}, supports_credentials=True) # support_credentials=True allows cookies to be sent with requests from the frontend and if using JWT tokens then I'll have to use other methods to store the token in the frontend like local storage or session storage.

@app.route("/api/")
def index():
    print("REQUEST MADe")
    return "Hellow world"


if __name__=="__main__":
    app.run(debug=True)