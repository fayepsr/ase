import flask
import json
import sys
from flask import request, abort
from datetime import datetime
import pytz

import highlight
import accuracy_check
import persist_model

app = flask.Flask(__name__)
app.config["DEBUG"] = True


"""
test-endpoint to check if flask is working

Args:
user: string that will be printed

Returns:
ob: json with name of user inside

Example Request:
http://localhost:5000/?user=charl
"""
@app.route('/', methods=['GET'])
def test():
    user = request.args.get('user')
    ob = {'user' : user}
    return json.dumps(ob, indent=4)


"""
Highlights code in a given language

Args:
code_to_format: code that should be formatted
language: language the code is in. possible values: python, java, kotlin

Returns:
result: json with prediction and tokens (tokens = result)
{'ok': 1, 'prediction': prediction, 'result': result}

Exceptions:
500: BaseLearnerException
"""
@app.route('/predict', methods=['GET'])
def api_predict():
    try:
        code_to_format = request.args.get('code_to_format')
        language = request.args.get('language')
        res = highlight.predict(code_to_format, language)
        if res['ok'] != 1:
            raise ValueError(res['msg'])
        result = json.dumps(res, indent=4)
        return result
    except ValueError as e:
        message = "BaseLearnerException " + str(e)
        # creating/opening a file
        f = open("errorlog.txt", "a")
 
        # writing in the file
        timezone = pytz.timezone('Europe/Madrid')
        f.write(str(datetime.now(tz = timezone))+" BaseLearnerException " + str(e) +"\n")
      
        # closing the file 
        f.close()
        abort(500, message) 
    return result



"""
fine-tunes the model with the code given

Args:
code_to_format: code that should be formatted
language: language the code is in. possible values: python, java, kotlin

Returns:
result: json with prediction and tokens (tokens = result)
{'ok': 1, 'prediction': prediction, 'result': result}

Exceptions:
500: BaseLearnerException
"""
@app.route('/finetune', methods=['GET'])
def api_finetune():
    try:
        code_to_format = request.args.get('code_to_format')
        language = request.args.get('language')
        res = highlight.finetune(code_to_format, language)
        if res['ok'] != 1:
            raise ValueError(res['msg'])
        result = json.dumps(res, indent=4)
        return result
    except ValueError  as e:
        message = "BaseLearnerException " + str(e)
        # creating/opening a file
        f = open("errorlog.txt", "a")
 
        # writing in the file
        timezone = pytz.timezone('Europe/Madrid')
        f.write(str(datetime.now(tz = timezone))+" BaseLearnerException " + str(e) +"\n")
      
        # closing the file
        f.close()
        abort(500, message)



"""
get the accuracy of the models

Args:
model_type: base, finetuning
language: language the code is in. possible values: python, java, kotlin

Returns:
result: json with prediction and tokens (tokens = result)
{'ok': 1, 'prediction': prediction, 'result': result}

Exceptions:
500: BaseLearnerException
"""
@app.route('/accuracy', methods=['GET'])
def api_accuracy():
    try:
        model_type = request.args.get('model_type')
        language = request.args.get('language')
        res = accuracy_check.check_accuracy(model_type, language)
        if res['ok'] != 1:
            raise ValueError(res['msg'])
        result = json.dumps(res, indent=4)
        return result
    except ValueError as e:
        message = "BaseLearnerException " + str(e)
        # creating/opening a file
        f = open("errorlog.txt", "a")
 
        # writing in the file
        timezone = pytz.timezone('Europe/Madrid')
        f.write(str(datetime.now(tz = timezone))+" BaseLearnerException " + str(e) +"\n")
      
        # closing the file
        f.close()
        abort(500, message)


"""
persists the model that is given via filename

Args:
filename: .pt model like java_base_model.pt, kotlin_finetuning.pt

Returns:
result: json with ok or error
"""


@app.route('/persist', methods=['POST'])
def api_persist():

    filename = request.args.get('filename')
    res = persist_model.persist_model(filename)
    return res


app.run(debug=True,host='0.0.0.0', port=9007)