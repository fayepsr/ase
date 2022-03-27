# shell_exec_python_from_php

This example shows how to run a python script using PHP. 


## Installation

```bash
docker build -f .\Dockerfile.dockerfile -t shell_exec_python_from_php:1.0 .
docker-compose -f .\shell_exec_python_from_php.yaml up
```
In case of Windows OS simply run 
```bash
.\shell_exec_python_from_php.bat
```

## Usage

Visit http://localhost:8089/python_exec.php on your browser and a "Python executed successfully" message should be executed


### Added java execution
Visit http://localhost:8089/java_exec.php on your browser and a "Hello, World!" message should be executed


## How it works

### PHP & python
We have created a PHP method python_exec.php which just shell_exec a command that executes python.
```php
$command = escapeshellcmd('python2.7 /home/python_example/test.py');
$output = shell_exec($command);
echo $output;
```


### Docker
In order to run PHP from one's browser a WebServer is needed. We use apache.

Dockerfile
We create a docker image FROM php:7.4-apache. 
We copy the python and PHP files.
We install python using the RUN command.

### AWS lightsail
To push the image to Amazon lightsail
```bash
aws lightsail  push-container-image --service-name ase-service-1 --label example_container --image shell_exec_python_from_php:1.0   
```
Our public domain https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/python_exec.php & https://ase-service-1.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/java_exec.php