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

    # Choose language
    if language == 'python':
        model = bl.SHModel(bl.PYTHON3_LANG_NAME, 'base_model')
        Python3Resolver = jpype.JClass("resolver.Python3Resolver")
        resolver = Python3Resolver()
    elif language == 'java':
        model = bl.SHModel(bl.JAVA_LANG_NAME, 'base_model')
        JavaResolver = jpype.JClass("resolver.JavaResolver")
        resolver = JavaResolver()
    elif language == 'kotlin':
        model = bl.SHModel(bl.KOTLIN_LANG_NAME, 'base_model')
        KotlinResolver = jpype.JClass("resolver.KotlinResolver")
        resolver = KotlinResolver()
    else:
        return {'ok': -1, 'msg': 'Not yet accepting this language'}

    # Do prediction
    model.setup_for_prediction()
    content = base64.b64decode(content).decode('UTF-8')
    lToks = resolver.lex(content)

    if isinstance(lToks, JArray):
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
    return {'ok': -1}


def finetune(content, language='python'):

    # JPype is used to access the Java FormalModel library
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['SHOracle.jar'])

    if language == 'python':
        model = bl.SHModel(bl.PYTHON3_LANG_NAME, 'finetuning_model')
        Python3Resolver = jpype.JClass("resolver.Python3Resolver")
        resolver = Python3Resolver()
    elif language == 'java':
        model = bl.SHModel(bl.JAVA_LANG_NAME, 'finetuning_model')
        JavaResolver = jpype.JClass("resolver.JavaResolver")
        resolver = JavaResolver()
    elif language == 'kotlin':
        model = bl.SHModel(bl.KOTLIN_LANG_NAME, 'finetuning_model')
        KotlinResolver = jpype.JClass("resolver.KotlinResolver")
        resolver = KotlinResolver()
    else:
        return {'ok': '-1', 'msg': 'Not yet accepting this language'}

    model.setup_for_finetuning()
    content = base64.b64decode(content).decode('UTF-8')
    hToks = resolver.highlight(content)

    if isinstance(hToks, JArray):
        tokenIds = []
        hCodeValues = []

        for hTok in hToks:
            tokenIds.append(hTok.tokenId)
            hCodeValues.append(hTok.hCodeValue)

        model.finetune_on(tokenIds, hCodeValues)
        model.persist_model()
        return {'ok': 1}
    return {'ok': -1}
