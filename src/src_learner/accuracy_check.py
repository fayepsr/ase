"""
Checks the accuracy of the model against the FormalModel

"""

from curses.ascii import HT
import SHModelUtils as bl
import argparse
import sys
import jpype
import jpype.imports
from jpype.types import *
from pathlib import Path

def check_accuracy(model_type, language):

    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['SHOracle.jar'])

    # Choose model type
    if model_type == "base":
        model_name = "base_model"
    elif model_type == "finetuning":
        model_name = "finetuning_model"
    else:
        return {'ok': -1, 'msg': 'This model type does not exist. Please select base or finetuning'}


    # Choose language
    if language == 'python':
        model = bl.SHModel(bl.PYTHON3_LANG_NAME, model_name)
        Python3Resolver = jpype.JClass("resolver.Python3Resolver")
        resolver = Python3Resolver()
        ext = '*.py'
    elif language == 'java':
        model = bl.SHModel(bl.JAVA_LANG_NAME, model_name)
        JavaResolver = jpype.JClass("resolver.JavaResolver")
        resolver = JavaResolver()
        ext = '*.java'
    elif language == 'kotlin':
        model = bl.SHModel(bl.KOTLIN_LANG_NAME, model_name)
        KotlinResolver = jpype.JClass("resolver.KotlinResolver")
        resolver = KotlinResolver()
        ext = '*.kt'
    else:
        return {'ok': -1, 'msg': 'Not yet accepting this language'}

    data_directory = './accuracyTestData/' + language


    model.setup_for_prediction()

    total_correct_files = 0
    total_correct_tokens = 0
    total_files = 0
    total_tokens = 0

    # Iterate through the Python source files in the provided directory and subdirectories
    for file in Path(data_directory).rglob(ext):
        try:
            content = file.read_text()
        except Exception:
            continue
        else:
            # Use the FormalModel's highlight method on the source code content
            hToks = resolver.highlight(content)

            # Extract tokenIds and hCodeValues from the resulting hToks and use them as input for
            # fine-tuning the model
            if isinstance(hToks, JArray):
                total_files += 1
                tokenIds = []
                hCodeValues = []

                for hTok in hToks:
                    total_tokens += 1
                    tokenIds.append(hTok.tokenId)
                    hCodeValues.append(hTok.hCodeValue)

                prediction = model.predict(tokenIds)

                # Compares the tokens for each file
                for j in range(len(hCodeValues)):
                    if prediction[j] == hCodeValues[j]:
                        total_correct_tokens += 1

                if prediction == hCodeValues:
                    total_correct_files += 1

    # Calculates the accuracy based on each correctly highlighted file's tokens
    if total_files > 0:
        #accuracy = total_correct_files / total_files
        accuracy = total_correct_tokens / total_tokens
    else:
        accuracy = 0
    return {'ok': 1, 'accuracy': accuracy, 'total_tokens': total_tokens, 'total_correct_tokens': total_correct_tokens}
