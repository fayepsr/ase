import highlight
import flask
import json
import sys
from flask import request, abort

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def test():
    user = request.args.get('user')
    ob = {'user' : user}
    return json.dumps(ob, indent=4)

@app.route('/predict', methods=['POST'])
def api_predict():
    try:
        print("hello") 
        code_to_format = request.form.get('code_to_format')
        language = request.form.get('language')
        res = highlight.predict(code_to_format, language)
        if res['ok'] != 1:
            raise ValueError(res['msg'])
        result = json.dumps(res, indent=4)
    except ValueError as e:
        #TODO: Add to error_log
        message = "BaseLearnerException " + str(e)
        abort(500, message)
    return result

@app.route('/finetune', methods=['POST'])
def api_finetune():
    try:
        code_to_format = request.form.get('code_to_format')
        language = request.form.get('language')
        res = highlight.finetune(code_to_format, language)
        if res['ok'] != 1:
            raise ValueError(res['msg'])
        result = json.dumps(res, indent=4)
    except ValueError  as e:
        #TODO: Add to error_log
        message = "BaseLearnerException " + str(e)
        abort(500, message)
    return result



app.run(debug=True,host='0.0.0.0', port=9007)