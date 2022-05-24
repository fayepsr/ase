import flask
import json
from flask import request, abort
from datetime import datetime
import pytz

import highlight
import accuracy_check
import persist_model

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def test():
    """
    test-endpoint to check if flask is working
    Example Request:
    http://localhost:5000/?user=charl

    @param user: string that will be printed
    @return: json with name of user inside
    """
    user = request.args.get('user')
    ob = {'user' : user}
    return json.dumps(ob, indent=4)


@app.route('/predict', methods=['POST'])
def api_predict():
    """
    Highlights code in a given language
    @param code_to_format: code that should be formatted
    @param language: language the code is in. possible values: python, java, kotlin
    @return: json with prediction and tokens (tokens = result) {'ok': 1, 'prediction': prediction, 'result': result}
    """
    try:
        code_to_format = request.form.get('code_to_format')
        language = request.form.get('language')
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


@app.route('/finetune', methods=['POST'])
def api_finetune():
    """
    fine-tunes the model with code that has been previously saved
    @param language: language the code is in. possible values: python, java, kotlin
    @return: message with status whether finetuning was successful or not
    """
    try:
        language = request.form.get('language')
        res = highlight.finetune(language)
        if res['ok'] < 0:
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

@app.route('/persist', methods=['POST'])
def api_persist():
    """
    persists the model that is given via filename

    @param filename: .pt model like java_base_model.pt, kotlin_finetuning.pt
    @return: json with ok or error
    """
    filename = request.args.get('filename')
    res = persist_model.persist_model(filename)
    return res


app.run(debug=True,host='0.0.0.0', port=9007)