# php:7.4-apache Container
This is the container that will implement the Rest API that will be used by the customers. Read more fot the API [here](../../README.md)
The Web Server set up is Apache. The programming language that works with apache on this container is PHP. 

## The dockerfile
Our dockerfile apart from copying the necessary file, installs the [PHP composer](https://getcomposer.org/doc/00-intro.md). This tool was used to install the library "phpunit" during testing.

## .htaccess 
We have created an [htaccess](./var/www/html/.htaccess) file that will redirect all requests except for download_logs to to public/index.php 

## download_logs.php
We needed an easy way to download out log files. Executing this url will download in a zip file all logs. 
*This comment would not exist in a real application. The url is http://localhost:8089/download_logs.php?secret=52r7$%^Gjj38*

## index.php
Our [index.php](./var/www/html/public/index.php) accepts three endpoints highlight, finetune, app_health(necessary endpoint for the lightsail container). Itwill call the appropriate function from the class Api. 

## classes/Api.class.php
This class holds the main functionality of the container. Here are some key points: 
- get_learner_url: According to the $_SERVER['SERVER_NAME'], we find whether the container with the model is in lightsail or localhost.
- the public functions are highlight and finetune. 
- the highlight endpoint always send the input code to the model for highlighting as well as finetuning. The container with the model is then responsible to decide whether it can be used for training. 

## classes/Logger.class.php
We decided to have a centralized global implementation for logging

## The tests
The source code for our tests is inside the folder tests/tests. They are based on [PHPUnit 9](https://phpunit.de/getting-started/phpunit-9.html). 
An interesting point in tests is the autoload.php which loads all the classes automatically. 


The tests are run via a Github action. 
You can run them from inside the container using the folowing commands 
```
cd tests
composer require --dev phpunit/phpunit ^9
export PATH=/tests/vendor/bin/:$PATH
phpunit --bootstrap ./autoload.php tests
```
## The documentation
A short documentation of the public interface of our classes is [here](documentation.md)
Alternatively, the original documentation from phpDocumentor is [here](./docs/index.html) . You need to open the html file from your browser.


We created the documentation using phpDocumentor using the folllowing commands: 
```
composer require onspli/phpdoc-markdown
wget https://phpdoc.org/phpDocumentor.phar
chmod +x phpDocumentor.phar
phpDocumentor  -d ./classes/  -t ./docs --title="PHP Documentation" --template=vendor/onspli/phpdoc-markdown/templates/public-onefile
```