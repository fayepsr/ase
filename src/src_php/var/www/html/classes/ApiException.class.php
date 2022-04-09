<?php 

    class ApiException extends Exception{
        //TODO: Set default code and message
        public function __construct($code , $message){
            http_response_code($code);
            print json_encode(array('msg'=>$message));
        }        

    }

    class ApiExceptionHTML extends Exception{
        //TODO: Set default code and message
        public function __construct($code , $html){
            http_response_code($code);
            print ($html);
        }        

    }