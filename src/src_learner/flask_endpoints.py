import highlight
import flask
import json
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
        code_to_format = request.form.get('code_to_format')
        language = request.form.get('language')
        result = json.dumps(highlight.predict(code_to_format), indent=4)
    except Exception as exc :
        #TODO: Add to error_log
        #message = "BaseLearnerException "+ str(exc)
        abort(500)
    return result

@app.route('/finetune', methods=['POST'])
def api_finetune():
    try:
        code_to_format = request.form.get('code_to_format')
        language = request.args.get('language')
        return json.dumps(highlight.finetune(code_to_format, language), indent=4)
    except Exception as exc :
        #TODO: Add to error_log
        #message = "BaseLearnerException "+ str(exc)
        abort(500)
    return result



app.run(debug=True,host='0.0.0.0', port=9007)