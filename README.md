## Rest API 

You may find in postman\ASE.postman_collection the collection of our Rest API. 
There are two endpoints exposed: Finetune and Predict
The code to be used for training or to highlight must be given base64encoded. 
Example executions are described below. 

### Finetune
curl --location --request POST 'http://localhost:8089/api/v1/finetune' \
--form 'lang="python"' \
--form 'code="cHJpbnQoIjEyMyIp"'

*cHJpbnQoIjEyMyIp is the python code base64encoded*
### Predict
curl --location --request POST 'http://localhost:8089/api/v1/highlight' \
--form 'lang="python"' \
--form 'code="cHJpbnQoIjEyMyIp"'

*cHJpbnQoIjEyMyIp is the python code base64encoded*


### Docker
To compose the container navigate inside src and run .\build_and_run_all.bat
See docker.md for more details.

### AWS lightsail
To push the images to Amazon lightsail we run .\lightsailpush.bat
Our public domain https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/
