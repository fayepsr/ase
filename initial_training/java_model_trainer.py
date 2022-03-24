"""
Trains a Java BaseLearner model, given a directory of the training data set, and produces a
fine-tuned model 'java_base_model.pt' in the current directory.

Example:
    $ python java_model_trainer.py ./training_data/java
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
JavaResolver = jpype.JClass("resolver.JavaResolver")


def main(data_directory: str):
    model = bl.SHModel(bl.JAVA_LANG_NAME, 'base_model')
    resolver = JavaResolver()
    ext = '*.java'

    model.setup_for_finetuning()

    # Iterate through the Java source files in the provided directory and subdirectories
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
        description='Train the base learner model for Java')
    parser.add_argument('training_data', type=str,
                        help='Path to directory of training data')
    args = parser.parse_args()
    main(args.training_data)
    sys.exit()
