import SHModelUtils as bl
import argparse
import sys
import jpype
import jpype.imports
from jpype.types import *
from pathlib import Path
import os
import json
import base64

def predict(code_to_format, language='python'):

    #os.chdir('/src_learner/')
    # JPype is used to access the Java FormalModel library
    jpype.startJVM(classpath=['SHOracle.jar'])
    Python3Resolver = jpype.JClass("resolver.Python3Resolver")

    model = bl.SHModel(bl.PYTHON3_LANG_NAME, 'base_model')
    resolver = Python3Resolver()
    model.setup_for_prediction()

    content = code_to_format
    content = base64.b64decode(content).decode('UTF-8')

    lToks = resolver.lex(content)

    if (isinstance(lToks, JArray)):
        tokenIds = []
        result = []

        for i in range(lToks.length):
            tokenIds.append(lToks[i].tokenId)
            result.append(
                {
                    "startIndex": lToks[i].startIndex,
                    "endIndex": lToks[i].endIndex,
                    "lItemtokenId": lToks[i].tokenId
                }
            )

        prediction = model.predict(tokenIds)
        return {'ok': 1, 'prediction': prediction, 'result': result}
    return {'error': -1}

# predict("YSA9IDAKZm9yIGkgaW4gcmFuZ2UoMTApOgogICAgYSs9MQo=")
