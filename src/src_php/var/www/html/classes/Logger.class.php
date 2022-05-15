<?php

//https://stackoverflow.com/questions/18673941/php-implement-logging-mechanism-to-file-in-several-classes
class Logger
{
    const INFO = 'info';
    const ERROR = 'error';

    private static $instance;
    private $config = array();

    private function __construct()
    {
        $this->config = require "/var/www/html/log_config.php";
    }

    private static function getInstance()
    {
        if (!self::$instance) {
            self::$instance = new Logger();
        }
        return self::$instance;
    }

    private function writeToFile($message)
    {
        if(!file_exists($this->config['log_file'])){
            file_put_contents($this->config['log_file'], "$message\n");
        }
        else{
            file_put_contents($this->config['log_file'], "$message\n", FILE_APPEND);
        }
        
    }

    public static function log($message, $level = Logger::INFO)
    {
        $date = date('Y-m-d H:i:s');
        $severity = "[$level]";
        $message = "$date $severity :: $message";
        self::getInstance()->writeToFile($message);
    }
}
