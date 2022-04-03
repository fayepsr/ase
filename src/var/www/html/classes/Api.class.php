<?php

class api{

    public static function highlight($lang = '', $code = ''){

        if(empty($lang) || empty($code)){
            throw new ApiException(406, "Invalid Input Arguments");
        }

        if(strtolower($lang) != "java" && strtolower($lang) != "kotlin" && strtolower($lang) != "python"){
            throw new ApiException(406, "Invalid Input Programming Language");
        }

        //escapeshellcmd wil add slashed to what needs to be escaped. For that we encoded it with base64_encode  
        $command = escapeshellcmd('python3.9 /home/src_python/highlight.py \''. base64_encode($code) .'\'');
        $output = shell_exec($command);
        echo $output;
        
        return array('resp' => "Formatted Input");

    }
}