# Welcome to the learner microservice documentation!

The learner microservice provides the core logic of highlighting for the whole
application.

## Architecture and Programming Languages

The learner microservice consists of the following components:

### The Flask Endpoints: flask_enpoints.py

Provides RESTful endpoints that wrap the functionalities such as predicting and
finetuning for the languages python, kotlin and java.

### The highlighting script: highlight.py

<<<<<<< HEAD
Implements the predict and finetune functionality by calling the BaseLearner and
FormalModel. TODO: More information, how is this working exactly

### helper scripts: accuracy_check.py, update_model.py, persist_model.py
=======
Implements the predict and finetune functionality using the BaseLearner and FormalModel.
Highlighting the input requests is done using the 'predict' function. It stores the input request for
future training/testing and returns the highlighted tokens from the 'base_model' for the language. Finetuning
is done usingthe 'finetune' function. If there are a minimum number of training samples (to be set as 100),
the training and test sets are loaded and the samples are checked for over laps with any archived training or
test samples using the helper functions 'load_training_set', 'load_test_set' and 'check_overlap'.
Then, the 'finetuning_model' is trained on the training set and its accuracy is compared with the 'base_model'
on the test set using a helper function called check_accuracy. If the 'finetuning_model' has a higher accuracy
than the 'base_model', it replaces the 'base_model' (helper function - 'exchange_models'), and the training
and test sets are archived (helper function - 'archive_training_samples').

### helper script: persist_model.py
>>>>>>> c33f8c1061a8dc5348b0cb4e607963fb91d8bbbc

From time to time, the weights of the model that is currently used for
prediction get swapped with the weights of the finetuned model. This process is
implemented in the update_model.py which also uses the accuracy_check.py for
this. The persist_model.py class can be used to persist the weights on lightsail
via an S3 container.

### FormalModel

This statistical model for syntax highlighting was provided to us as a black-box model. It is included as the java
library 'SHOracle.jar'.
"This Java library allows for the formal computation of syntax highlighting patterns of input programs.
Hence, syntax highlighting is computed by analysing the Abstract Syntax Tree (AST) corresponding to the input
provided. Although for the derivation of the AST some minor imprecision are allowed, a high level of 
grammatical errors in the language derivation provided will lead this process to fail gracefully. The library
supports Java (1.8 or later), Python (3.x or later) and Kotlin (1.x or later)."
Source for more details - https://github.com/MEPalma/UZH-ASE-AnnotationWS-FormalModel

### BaseLearner

This deep learning model for syntax highlighting implements a bidirectional RNN with an embedding layer and
a hidden layer of dimensions 128 and 32 respectively. It was provided to us a black-box model. It is included
as the python script 'SHModelUtils.py'.
Source for more details - https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner

### .pt files

Save the weights of the trained models. Weights that are currently used for
prediction are saved in files with the "base" tag. Weights that currently
finetuned are saved in files with the "finetuning" tag.

## Motivation for used Technologies

<<<<<<< HEAD
The FormalModel and BaseLearner are written in the programming languages Java
and Python. Since we considered these two applications as blackboxes, we did not
change anything about their respective implementation. Instead, we decided to
make the functionalities of these two applications accessible via a standardised
interface. As most of our team members are familiar with Python, we decided to
write the interface in Python. For the endpoints itself we used the popular
framework "Flask" as the framework is easy to use and has an extensive
documentation. The highlight and finetuning functionalities were implemented
with the help of JPype, a Python module that enables access to Java libraries
from within Python. We decided to use JPype because it is easy to use,
well-documented, and allows us to use the provided FormalModel library in Java
from within our Python components.

We also used the boto3 software-development kit for the persistence of the model
weights (the .pt files), as this is the official SDK provided by AWS for the
interaction with its cloud services such as the stoarge service s3. For testing,
we used the unittest library of the Python since we were familiar with it and it
is easy to use. For logging we implemented the error logging functionality for
PHP code and for the python code. Whenever an error in the input is detected, an
error log file is created which with some information about the error such as
time, error message received, etc. This would help the users detect why the
program might not have worked with a certain input.
=======
The FormalModel and BaseLearner are written in the programming languages Java and Python. Since we considered 
these two applications as blackboxes, we did not change anything about their respective implementation. Instead,
we decided to make the functionalities of these two applications accessible via a standardised interface. As most of our
team members are familiar with Python, we decided to write the interface in Python. For the endpoints itself we used
the popular framework "Flask" as the framework is easy to use and has an extensive documentation. TODO: please check:
The implementation of the highlight and finetuning functionality was straightforward since python provides the possibility
to interact with java code via the jpype library. (Why did we use this library?)
We also used the boto3 software-development kit for the persistence of the model weights (the .pt files), as this is the
official SDK provided by AWS for the interaction with its cloud services such as the stoarge service s3.
For testing, we used the unittest library of the Python since we were familiar with it and it is easy to use. 
For logging we implemented the error logging functionality for PHP code and for the python code. Whenever an error in the
input is detected, an error log file is created which with some information about the error such as time, error message
received, etc. This would help the users detect why the program might not have worked with a certain input.
>>>>>>> c33f8c1061a8dc5348b0cb4e607963fb91d8bbbc

## Core Functionalities

- Highlighting of the Java, Python and Kotlin Code via a neural network (the
  BaseLearner with .pt base weights)
- Finetuning of a copy of the neural network (BaseLearner with .pt finetuning
  weights)
- Model update by replacing the base weights with the finetuning weights if the
  finetuning weights pass a certain accuracy threshhold
- Accuracy checking functionality: collects files which have not been used for
  training and assesses model accuracy based on these files
- Weights can be persisted via an S3 bucket when microservice is running in the
  cloud

## Requests

Requests are handled via a RESTful Flask API. The following core requests are
available:

/predict

Args: code_to_format: code that should be formatted language: language the code
is in. possible values: python, java, kotlin

/finetune

Args: code_to_format: code that should be formatted language: language the code
is in. possible values: python, java, kotlin

For more info, see the documentation of flask_endpoints.py

## Tests

The unittests for the learner microservice can be found in the folder tests.
They are written with the help of pythons built-in library "unittest". The tests
can be run with the following command:

python -m unittest discover /src/tests

## Run the Microservice

There are three possibilities to run the learner microservice.

Via Docker:

Create a new image for the dockerfile provided in the src_learner folder. Start
the container and interact with the application by sending requests to
http://localhost:5000/.

Via Local Machine:

Please make shure you have Python version 3.9 and Java version 17.0.2 installed.
Also make shure to install all Python packages that are specified in the
requirements.txt file. After that, you can start the application locally by
running the "flask_endpoints.py" file and sending requests to
http://localhost:9070/

Via the Cloud:

The endpoints of this container are not publicly available on the deployed
version on lightsail as users interact with the application via the php
endpoints.

## Documentation

TODO
