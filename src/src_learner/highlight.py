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
import numpy as np
import shutil


def model_loader(language, name):
    """

    @param name: 'base_model' or 'finetuning_model'
    @param language: language for which to load the model
    @return: model
    """
    # Choose language and load appropriate base_model
    if language == 'python':
        model = bl.SHModel(bl.PYTHON3_LANG_NAME, name)
    elif language == 'java':
        model = bl.SHModel(bl.JAVA_LANG_NAME, name)
    elif language == 'kotlin':
        model = bl.SHModel(bl.KOTLIN_LANG_NAME, name)
    else:
        return {'ok': -1, 'msg': 'Not yet accepting this language'}
    return model

def resolver_loader(language):
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['/src/SHOracle.jar'])
    """
    Load the resolver
    @param language: python, java, kotlin
    @return:
    """
    # Choose language and load appropriate base_model
    if language == 'python':
        Python3Resolver = jpype.JClass("resolver.Python3Resolver")
        resolver = Python3Resolver()
    elif language == 'java':
        JavaResolver = jpype.JClass("resolver.JavaResolver")
        resolver = JavaResolver()
    elif language == 'kotlin':
        KotlinResolver = jpype.JClass("resolver.KotlinResolver")
        resolver = KotlinResolver()
    else:
        return {'ok': -1, 'msg': 'Not yet accepting this language'}
    return resolver

def predict(content, language='python'):
    """
        Highlights code given for a specific language.

        @param content: code to highlight
        @param language: python, kotlin, java
        @return: highlighted code (word + highlight class)
    """

    # JPype is used to access the Java FormalModel library
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['/src/SHOracle.jar'])

    if not (language == 'python' or language == 'java' or language == 'kotlin'):
        return {'ok': -1, 'msg': 'not yet accepting this language'}

    model = model_loader(language, 'base_model')
    resolver = resolver_loader(language)

    # Do prediction & save input as train/test sample with a 90/10 probability
    model.setup_for_prediction()
    content = base64.b64decode(content).decode('UTF-8')
    hToks = resolver.highlight(content)
    if isinstance(hToks, JArray):
        tokenIds = []
        hCodeValues = []
        result = []

        for i in range(hToks.length):
            tokenIds.append(hToks[i].tokenId)
            hCodeValues.append(hToks[i].hCodeValue)
            result.append(
                {
                    "startIndex": hToks[i].startIndex,
                    "endIndex": hToks[i].endIndex,
                    "lItemtokenId": hToks[i].tokenId
                }
            )

        prediction = model.predict(tokenIds)

        # Store content for finetuning
        decide_traintest = np.random.random_sample()
        if decide_traintest < 0.9:
            # Store tokenIds and hCodes in training set
            filepath = "/src/trainingData/" + language + "/training_current.txt"
        else:
            # Store tokenIds and hCodes in training set
            filepath = "/src/accuracyTestData/" + language + "/test_current.txt"
        with open(filepath, 'a+', encoding="utf-8") as f:
            f.write(','.join(map(str, tokenIds)) + ':' +
                    ','.join(map(str, hCodeValues)) + '\n')

        return {'ok': 1, 'prediction': prediction, 'result': result}
    return {'ok': -1}

def load_training_set(path):
    """
    Initializes the training set based on the programming language given

    @param path: path to the file that should be opened
    @return: txt_training_current
    """
    try:
        with open(path, 'rt', encoding='utf-8') as f_training_current:
            txt_training_current = f_training_current.read().splitlines()
    except FileNotFoundError:
        txt_training_current = []
    return txt_training_current

def load_test_set(path):
    """
    Initializes the test set based on the programming language given

    @param path: path to the file that should be opened
    @return: txt_test_current
    """
    try:
        # Read the current test set
        with open(path, 'rt', encoding='utf-8') as f_test_current:
            txt_test_current = f_test_current.read().splitlines()
    except FileNotFoundError:
        txt_test_current = []
    return txt_test_current

def check_overlap(txt_training_current, txt_test_current, language, training_directory='', training_current_path='', test_directory='', test_current_path=''):
    if not training_directory:
        training_directory = "/src/trainingData/" + language
    if not training_current_path:
        training_current_path = training_directory + "/training_current.txt"
    if not test_directory:
        test_directory = "/src/accuracyTestData/" + language
    if not test_current_path:
        test_current_path = test_directory + "/test_current.txt"

    num_training_samples = len(txt_training_current)
    num_test_samples = len(txt_test_current)

    # Remove overlaps between current training and test docs
    txt_training_current = [i for i in txt_training_current if i not in txt_test_current]

    # Remove duplicate token sequences from current training and test sets
    # already present in saved training sets
    training_filenum = 1
    while os.path.exists(training_directory + f'/training_{training_filenum}.txt'):
        with open(training_directory + f'/training_{training_filenum}.txt', 'rt',
                  encoding='utf-8') as f_train:
            training_set = f_train.read().splitlines()
        txt_training_current = [i for i in txt_training_current if i not in training_set]
        txt_test_current = [i for i in txt_test_current if i not in training_set]
        training_filenum += 1

    # Remove duplicate token sequences from current training and test sets
    # already present in saved test sets
    test_filenum = 1
    while os.path.exists(test_directory + f'/test_{test_filenum}.txt'):
        with open(test_directory + f'/test_{test_filenum}.txt', 'rt',
                  encoding='utf-8') as f_test:
            test_set = f_test.read().splitlines()
        txt_training_current = [i for i in txt_training_current if i not in test_set]
        txt_test_current = [i for i in txt_test_current if i not in test_set]
        test_filenum += 1

    # Check if the number of training samples have decreased and update the file
    if num_training_samples > len(txt_training_current):
        num_training_samples = len(txt_training_current)

        if num_training_samples == 0:
            os.remove(training_current_path)
        else:
            with open(training_current_path, 'w', encoding="utf-8") as f_training_current:
                f_training_current.write("\n".join(txt_training_current))

    # Check if the number of test samples has decreased and update the file
    if num_test_samples > len(txt_test_current):
        num_test_samples = len(txt_test_current)

        if num_test_samples == 0:
            os.remove(test_current_path)
            # replace the current test with an archived one for testing after training
            txt_test_current = test_set
        else:
            with open(test_current_path, 'w', encoding="utf-8") as f_test_current:
                f_test_current.write("\n".join(txt_test_current))

    return {'training_current': txt_training_current,
            'test_current': txt_test_current,
            'training_filenum': training_filenum,
            'test_filenum': test_filenum}

def check_accuracy(model, txt_test_current):
    model.setup_for_prediction()
    total_tokens = 0
    total_correct_tokens = 0

    # check that file is not empty
    if len(txt_test_current) == 0:
        return {'ok': -1, 'msg': 'file is empty'}

    # Test on test set
    split_test_current = [i.split(':') for i in txt_test_current]
    tokenId_set = [[int(token) for token in tokenRow[0].split(',')]
                   for tokenRow in split_test_current]
    hCodeValue_set = [[int(hCodeValue) for hCodeValue in hCodeValueRow[1].split(',')]
                      for hCodeValueRow in split_test_current]
    # check that we have the right amount of tokens and Ids
    if len(tokenId_set) != len(hCodeValue_set):
        return {'ok': -1, 'msg': 'tokens do not match hCode', 'len_tokenId': len(tokenId_set), 'len_hCode': len(hCodeValue_set)}

    for sample in range(len(tokenId_set)):
        prediction = model.predict(tokenId_set[sample])
        for hCodeValue in range(len(hCodeValue_set[sample])):
            total_tokens += 1
            hCodeValue_sample = hCodeValue_set[sample]
            if hCodeValue_sample[hCodeValue] == prediction[hCodeValue]:
                total_correct_tokens += 1

    if total_tokens > 0:
        accuracy = total_correct_tokens / total_tokens
    else:
        accuracy = 0

    return {'ok': 1, 'accuracy': accuracy, 'total_tokens': total_tokens, 'total_correct_tokens': total_correct_tokens}

def exchange_models(language, accuracy_base, accuracy_finetuning):
    """
        Replaces base model with finetuning model if accuracy is enough high

        @param language: python, java, kotlin
        @param accuracy_base: the accuracy of the base model
        @param accuracy_finetuning: the accuracy of the finetuning model
        @return: msg that explains if model was updated or not
    """
    # Model names for Python language have the prefix 'python3'
    if language == "python":
        language = language + "3"

    path_base_model = language + "_base_model.pt"
    path_finetune_model = language + "_finetuning_model.pt"

    # If accuracy has not decreased after training, replace the base model with
    # the fine-tuned model. Else, rollback training
    if accuracy_finetuning >= accuracy_base:
        try:
            os.remove(path_base_model)
            shutil.copyfile(path_finetune_model, path_base_model)
        except Exception as e:
            return {'ok': -1, 'exception': e}
        else:
            status_msg = f'Base Model updated. Accuracy: {accuracy_base} -> {accuracy_finetuning}'
            return status_msg
    else:
        try:
            os.remove(path_finetune_model)
            shutil.copyfile(path_base_model, path_finetune_model)
        except Exception as e:
            return {'ok': -1, 'exception': e}
        else:
            status_msg = f'No update. Accuracy: {accuracy_base} -> {accuracy_finetuning}'
            return status_msg

def archive_training_samples(training_directory_root, test_directory_root, txt_test_current, training_filenum, test_filenum):

    training_directory = training_directory_root
    training_current_path = training_directory + "/training_current.txt"
    test_directory = test_directory_root
    test_current_path = test_directory + "/test_current.txt"

    # Archive the current training samples
    shutil.copyfile(training_current_path, training_directory +
                    f'/training_{training_filenum}.txt')
    os.remove(training_current_path)

    # Archive the current test samples, if file is sufficiently large
    if len(txt_test_current) > 100:
        shutil.copyfile(test_current_path, test_directory +
                        f'/test_{test_filenum}.txt')
        os.remove(test_current_path)

def finetune(language='python', min_num_training_samples=100):
    """
    Finetunes the model based on the files in the folder trainingData

    @param language: python, java, kotlin
    @param min_num_training_samples: the minimum number of training samples, normally 100
    @return: dictionary with ok if finetuning was successful, error otherwise
    """
    training_directory = "/src/trainingData/" + language
    training_current_path = training_directory + "/training_current.txt"
    test_directory = "/src/accuracyTestData/" + language
    test_current_path = test_directory + "/test_current.txt"

    # Read the current training set
    txt_training_current = load_training_set(training_current_path)
    txt_test_current = load_test_set(test_current_path)

    # Check if there are at least min_num_training_samples to train on
    if len(txt_training_current) < min_num_training_samples:
        return {'ok': 0, 'msg': 'Not enough training samples 1'}

    # correct overlap if necessary
    result_check_overlap = check_overlap(txt_training_current, txt_test_current, language)
    txt_training_current = result_check_overlap.get('training_current')
    txt_test_current = result_check_overlap.get('test_current')
    training_filenum = result_check_overlap.get('training_filenum')
    test_filenum = result_check_overlap.get('test_filenum')

    # Check if there are at least min_num_training_samples to train on
    if len(txt_training_current) < min_num_training_samples:
        return {'ok': 0, 'msg': 'Not enough training samples 2'}

    # load models for training
    model = model_loader(language, 'finetuning_model')
    base_model = model_loader(language, 'base_model')

    model.setup_for_finetuning()

    # Train on training_current set
    num_epochs = 2
    split_training_current = [i.split(':') for i in txt_training_current]
    tokenId_set = [[int(token) for token in tokenRow[0].split(',')]
                   for tokenRow in split_training_current]
    hCodeValue_set = [[int(hCodeValue) for hCodeValue in hCodeValueRow[1].split(',')]
                      for hCodeValueRow in split_training_current]

    convergence_threshold = 0.01  # threshold for stopping epochs
    training_error = 1000  # initialize error with a high number
    for epoch in range(num_epochs):
        epoch_error = 0
        for sample in range(len(tokenId_set)):
            epoch_error = epoch_error + model.finetune_on(tokenId_set[sample], hCodeValue_set[sample])
            model.persist_model()
        if (training_error - epoch_error) < convergence_threshold:
            break
        training_error = epoch_error

    accuracy_finetuning_msg = check_accuracy(model, txt_test_current)
    accuracy_base_msg = check_accuracy(base_model, txt_test_current)

    if accuracy_finetuning_msg.get('ok') != 1:
        return accuracy_finetuning_msg
    elif accuracy_base_msg.get('ok') != 1:
        return accuracy_base_msg

    accuracy_finetuning = check_accuracy(model, txt_test_current).get('accuracy')
    accuracy_base = check_accuracy(base_model, txt_test_current).get('accuracy')

    # exchange models if accuracy is higher of finetuning_model than base model
    status_msg = exchange_models(language, accuracy_base, accuracy_finetuning)

    # archive samples
    archive_training_samples(training_directory, test_directory, txt_test_current, training_filenum, test_filenum)

    return {'ok': 1, 'msg': status_msg}
