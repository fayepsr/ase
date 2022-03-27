"""
Checks the accuracy of the model agaisnt the FormalModel

Run with - 
 $ python3 ./python_accuracy_checker.py ./testing_data

"""

from curses.ascii import HT
import BaseLearner.SHModelUtils as bl
import argparse
import sys
import jpype
import jpype.imports
from jpype.types import *
from pathlib import Path

# JPype is used to access the Java FormalModel library
jpype.startJVM(classpath=['../FormalModel/Library/SHOracle.jar'])
Python3Resolver = jpype.JClass("resolver.Python3Resolver")


def main(data_directory: str):
    model = bl.SHModel(bl.PYTHON3_LANG_NAME, 'base_model')
    resolver = Python3Resolver()
    ext = '*.py'

    data_directory = data_directory[2:]
    data_directory = '../'+ data_directory

    model.setup_for_prediction()

    total_correct_lines = 0
    total_lines = 0

    # Iterate through the Python source files in the provided directory and subdirectories
    for file in Path(data_directory).rglob(ext):
        try:
            content = file.read_text()
        except Exception:
            continue
        else:

            file_read = open(file, 'r')
            lines = file_read.readlines()

            # Reading single lines of code from the input file
            for line in lines:
            # Use the FormalModel's highlight method on the source code content
                total_lines += 1
                hToks = resolver.highlight(line)

                # Extract tokenIds and hCodeValues from the resulting hToks and use them as input for prediction
                if (isinstance(hToks, JArray)):
                    tokenIds = []
                    hCodeValues = []

                    for hTok in hToks:
                        tokenIds.append(hTok.tokenId)
                        hCodeValues.append(hTok.hCodeValue)

                    prediction = model.predict(tokenIds)
                    if prediction == hCodeValues:
                            total_correct_lines += 1


    # Calculates the accuracy of each line of code from an input test file
    # Check for each word? Check for each file?
    accuracy = total_correct_lines/total_lines
    print("Model accuracy is: ", accuracy)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the accuracy of the model for Python')
    parser.add_argument('testing_data', type=str, help='Path to directory of testing data')
    args = parser.parse_args()
    main(args.testing_data)
    sys.exit()
