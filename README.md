## Rest API 
You may find in [Postman Collection](postman/) the collection of our Rest API. 
You may find instructions as to how to import the postman collection [here](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/).
There are two endpoints exposed: Finetune and Predict
The code to be used for training or to highlight must be given base64encoded. 

## Wiki

We heave also created a Github Wiki with important documents such as the documentation of testing and project organisation.
You can find it here: https://github.com/fayepsr/ase/wiki
The wiki also contains:
- Project Organisation: https://github.com/fayepsr/ase/wiki/Project-Organization
- Testing: https://github.com/fayepsr/ase/wiki/Testing
- Microservice Overview: https://github.com/fayepsr/ase/wiki/Microservice-Overview

### Example api calls
*This comment would not exist in a real application. The secret to use is: hsdiwu8&%$$*

#### Finetune
curl --location --request POST 'http://localhost:8089/api/v1/finetune' \
--form 'lang="python"' \
--form 'code="cHJpbnQoIjEyMyIp"' \
--form 'secret="XXXXXXXX"'

*cHJpbnQoIjEyMyIp is the python code base64encoded*
#### Predict
curl --location --request POST 'http://localhost:8089/api/v1/highlight' \
--form 'lang="python"' \
--form 'code="cHJpbnQoIjEyMyIp"' \
--form 'secret="XXXXXXXX"' \
--form 'mode="json"'

- cHJpbnQoIjEyMyIp is the python code base64encoded
- mode: "json" or "html"
The html mode will return a full HTML document with agiven HTML class for each type of token. 
The json mode will return a json array as shown in the example below. Each element of the array is a token. 
    - startIndex, endIndex: refer to the position of the token in the code
    - token: is the token itself
    - type: ["GENERAL", "KEYWORD", "LITERAL", "CHAR_STRING_LITERAL", "COMMENT", "CLASS_DECLARATOR", "FUNCTION_DECLARATOR", "VARIABLE_DECLARATOR", "TYPE_IDENTIFIER", "FUNCTION_IDENTIFIER", "FIELD_IDENTIFIER", "ANNOTATION_DECLARATOR", "UNKONOWN"]
    - Example ```
    [
    {
        "startIndex": 0,
        "endIndex": 5,
        "type": "KEYWORD",
        "token": "import"
    },
    {
        "startIndex": 7,
        "endIndex": 10,
        "type": "GENERAL",
        "token": "java"
    },
    ....
] ```

## Docker
To compose the containers navigate inside src and run [.\build_and_run_all.bat](./src/build_and_run_all.bat) (for Windows Environments).

If not in a Windows Environment, you may run the following commands: 
```
cd src 
docker-compose down
docker image rm src_php:latest
docker image rm src_learner:latest
docker image rm src_react:latest
cd ./src_react
docker build -f ./dockerfile -t src_react:latest . 
cd ../src_php
docker build -f ./dockerfile -t src_php:latest .
cd ../src_learner
docker build -f ./dockerfile -t src_learner:latest .
cd ../
docker-compose up
```
## Our demo (docker-compose)

You can start the demo by navigating with the command line to the "src" folder in this repo and then type
"docker-compose up". The yaml file is called "docker-compose.yml". 

Our private domain for highlighting logic learner: http://learner:9007
Our public domain: http://localhost:8089/api/v1
Our demo frontend: http://localhost:3007

## Our demo (AWS lightsail)
Our public domain: https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/  
Our demo frontend: https://container-service-2.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/

We have scheduled an event using AWS eventbridge and the finetune function is called every 30 minutes. 

## Our Containers 
- [React](./src/src_ract/README.md)
- [PHP](./src/src_php/README.md)
- [python_JAVA](./src/src_learner/README.md)
