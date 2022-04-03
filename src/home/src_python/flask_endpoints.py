import highlight
import flask
import json
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def test():
    user = request.args.get('user')
    ob = {'user' : user}
    return json.dumps(ob, indent=4)

@app.route('/predict', methods=['GET'])
def api_predict():
    code_to_format = request.args.get('code_to_format')
    #language = request.args.get('language')
    return json.dumps(highlight.predict(code_to_format), indent=4)


app.run()