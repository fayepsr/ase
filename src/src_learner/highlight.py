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

def predict(content, language='python'):
 
    # JPype is used to access the Java FormalModel library
    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=['SHOracle.jar'])

    # Choose language and load appropriate base_model
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
            filepath = "trainingData/" + language + "/training_current.txt"
        else:
            #Store tokenIds and hCodes in training set
            filepath = "accuracyTestData/" + language + "/test_current.txt"
        with open(filepath, 'a+', encoding="utf-8") as f:
            f.write(','.join(map(str, tokenIds)) + ':' +
                    ','.join(map(str, hCodeValues)) + '\n')     
        
        return {'ok': 1, 'prediction': prediction, 'result': result}
    return {'ok': -1}


def finetune(language='python'):
    
    training_directory = "trainingData/" + language
    training_current_path = training_directory + "/training_current.txt"
    test_directory = "accuracyTestData/" + language
    test_current_path = test_directory + "/test_current.txt"
    min_num_training_samples = 100
    
    # Read the current training set
    with open(training_current_path, 'rt', encoding='utf-8') as f_training_current:
        txt_training_current = f_training_current.read().splitlines()
                                
    # Check if there are at least min_num_training_samples to train on
    if len(txt_training_current) < min_num_training_samples:
        return {'ok': -1, 'msg': 'Not enough training samples'}
    
    # Read the current test set
    with open(test_current_path, 'rt', encoding='utf-8') as f_test_current:
        txt_test_current = f_test_current.read().splitlines()
    
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
    
    # Check if the number of test samples have decreased and update the file
    if num_test_samples > len(txt_test_current):
        num_test_samples = len(txt_test_current)
        
        if num_test_samples == 0:
            os.remove(test_current_path)
            # replace the current test with an archived one for testing after training
            txt_test_current = test_set
        else:
            with open(test_current_path, 'w', encoding="utf-8") as f_test_current:
                f_test_current.write("\n".join(txt_test_current))
    
    # Check if there are at least min_num_training_samples to train on
    if len(txt_training_current) < min_num_training_samples:
        return {'ok': -1, 'msg': 'Not enough training samples'}           
    
    if language == 'python':
        model = bl.SHModel(bl.PYTHON3_LANG_NAME, 'finetuning_model')
        base_model = bl.SHModel(bl.PYTHON3_LANG_NAME, 'base_model')
    elif language == 'java':
        model = bl.SHModel(bl.JAVA_LANG_NAME, 'finetuning_model')
        base_model = bl.SHModel(bl.JAVA_LANG_NAME, 'base_model')
    elif language == 'kotlin':
        model = bl.SHModel(bl.KOTLIN_LANG_NAME, 'finetuning_model')
        base_model = bl.SHModel(bl.KOTLIN_LANG_NAME, 'base_model')
    else:
        return {'ok': '-1', 'msg': 'Not yet accepting this language'}

    model.setup_for_finetuning()
    
    # Train on training_current set
    num_epochs = 10
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
            epoch_error = epoch_error + model.finetune_on(tokenId_set[sample],hCodeValue_set[sample])
            model.persist_model()
        if (training_error - epoch_error) < convergence_threshold:
            break
        training_error = epoch_error
    
    # Test on test set
    split_test_current = [i.split(':') for i in txt_test_current]
    test_tokenId_set = [[int(token) for token in tokenRow[0].split(',')]
                        for tokenRow in split_test_current]
    test_hCodeValue_set = [[int(hCodeValue) for hCodeValue in hCodeValueRow[1].split(',')]
                           for hCodeValueRow in split_test_current]
    
    accuracy_finetuning = check_accuracy(model, test_tokenId_set, test_hCodeValue_set).get('accuracy')
    accuracy_base = check_accuracy(base_model, test_tokenId_set, test_hCodeValue_set).get('accuracy')
    
    # Model names for Python language have the prefix 'python3'
    if language == "python":
        language = language + "3"
        
    #cwd = os.getcwd()
    path_base_model = language + "_base_model.pt"
    path_finetune_model = language + "_finetuning_model.pt"
       
    # If accuracy has not decreased after training, replace the base model with
    # the fine-tuned model. Else, rollback training
    if accuracy_finetuning >= accuracy_base:
        try:
            os.remove(path_base_model)
            shutil.copyfile(path_finetune_model, path_base_model)
        except Exception as e:
            return {'ok' : -1, 'exception' : e}
        else:
            status_msg = f'Base Model updated. Accuracy: {accuracy_base} -> {accuracy_finetuning}'
    else:
        try:
            os.remove(path_finetune_model)
            shutil.copyfile(path_base_model, path_finetune_model)
        except Exception as e:
            return {'ok' : -1, 'exception' : e}
        else:
            status_msg = f'No update. Accuracy: {accuracy_base} -> {accuracy_finetuning}'
    
    # Archive the current training samples
    shutil.copyfile(training_current_path, training_directory +
                    f'/training_{training_filenum}.txt')
    os.remove(training_current_path)
    
    #Archive the current test samples, if file is sufficiently large
    if len(txt_test_current) > 100:
        shutil.copyfile(test_current_path, test_directory +
                        f'/test_{test_filenum}.txt')
        os.remove(test_current_path)   
    
    return {'ok': 1, 'msg': status_msg}

def check_accuracy(model, tokenId_set, hCodeValue_set):
    model.setup_for_prediction()
    total_tokens = 0
    total_correct_tokens = 0
    
    for sample in range(len(tokenId_set)):
        prediction = model.predict(tokenId_set[sample])
        for hCodeValue in range(len(hCodeValue_set[sample])):
            total_tokens += 1
            hCodevalue_sample = hCodeValue_set[sample]
            if hCodevalue_sample[hCodeValue] == prediction[hCodeValue]:
                total_correct_tokens += 1
    
    if total_tokens > 0:
        accuracy = total_correct_tokens/total_tokens
    else:
        accuracy = 0
    
    return {'ok': 1, 'accuracy': accuracy, 'total_tokens': total_tokens, 'total_correct_tokens': total_correct_tokens}
