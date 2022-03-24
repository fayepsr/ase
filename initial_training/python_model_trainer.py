"""
Trains a Python BaseLearner model, given a directory of the training data set, and produces a
fine-tuned model 'python3_base_model.pt' in the current directory.

Example:
    $ python python_model_trainer.py ./training_data/python
"""

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

    model.setup_for_finetuning()

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
            if (isinstance(hToks, JArray)):
                tokenIds = []
                hCodeValues = []

                for hTok in hToks:
                    tokenIds.append(hTok.tokenId)
                    hCodeValues.append(hTok.hCodeValue)

                model.finetune_on(tokenIds, hCodeValues)

    # Save the model
    model.persist_model()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Train the base learner model for Python')
    parser.add_argument('training_data', type=str,
                        help='Path to directory of training data')
    args = parser.parse_args()
    main(args.training_data)
    sys.exit()
