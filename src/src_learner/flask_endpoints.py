import highlight
import flask
import json
import sys
from flask import request, abort
from datetime import datetime
import pytz

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
        res = highlight.predict(code_to_format, language)
        if res['ok'] != 1:
            raise ValueError(res['msg'])
        result = json.dumps(res, indent=4)
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
    try:
        code_to_format = request.form.get('code_to_format')
        language = request.form.get('language')
        res = highlight.finetune(code_to_format, language)
        if res['ok'] != 1:
            raise ValueError(res['msg'])
        result = json.dumps(res, indent=4)
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
    return result



app.run(debug=True,host='0.0.0.0', port=9007)