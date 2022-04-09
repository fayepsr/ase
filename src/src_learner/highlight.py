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

def predict(content, language='python'):

    # JPype is used to access the Java FormalModel library
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['SHOracle.jar'])
    Python3Resolver = jpype.JClass("resolver.Python3Resolver")

    model = bl.SHModel(bl.PYTHON3_LANG_NAME, 'base_model')
    resolver = Python3Resolver()
    model.setup_for_prediction()

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


def finetune(content, language='python'):

    # JPype is used to access the Java FormalModel library
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['SHOracle.jar'])

    Python3Resolver = jpype.JClass("resolver.Python3Resolver")
    resolver = Python3Resolver()

    if (language == 'python'):
        model = bl.SHModel(bl.PYTHON3_LANG_NAME, 'finetuning_model')

    model.setup_for_finetuning()
    content = base64.b64decode(code_to_format).decode('UTF-8')
    hToks = resolver.highlight(content)

    if (isinstance(hToks, JArray)):
        tokenIds = []
        hCodeValues = []

        for hTok in hToks:
            tokenIds.append(hTok.tokenId)
            hCodeValues.append(hTok.hCodeValue)

        model.finetune_on(tokenIds, hCodeValues)
        model.persist_model()
        return {'ok': 1, 'result': hToks}
    return {'error': -1}