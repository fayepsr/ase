<?php

class api{

    public static function highlight($lang = '', $code = ''){

        if(empty($lang) || empty($code)){
            throw new ApiException(406, "Invalid Input Arguments");
        }

        if(strtolower($lang) != "java" && strtolower($lang) != "kotlin" && strtolower($lang) != "python"){
            throw new ApiException(406, "Invalid Input Programming Language");
        }

        
        return array('resp' => "Formatted Input");

    }
}