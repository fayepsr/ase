<?php

class api{

    //TODO: Maybe I should write them in a config file
    private static $learner_url = "http://learner:9007/" ; 

    public static function highlight($lang = '', $code = ''){

        if(empty($lang) || empty($code)){
            throw new ApiException(406, "Invalid Input Arguments");
        }

        if(strtolower($lang) != "java" && strtolower($lang) != "kotlin" && strtolower($lang) != "python"){
            throw new ApiException(406, "Invalid Input Programming Language");
        }

        try {
            $output = api::curl_post_exec("predict", array('code_to_format' => $code, 'language' => $lang));
        } catch (\Throwable $th) {
            throw new ApiExceptionHTML(500, $th->getMessage()  );
        }
       

        try {
            $full_HTML = api::getHTML(base64_decode($code), $output);
        } catch (\Throwable $th) {
            throw new ApiException(500, "api::getHTML error. Log: ". $th->getMessage());
        }
        
        
        
        return array('resp' => base64_encode($full_HTML));

    }

    public static function finetune($lang = '', $code = ''){

        if(empty($lang) || empty($code)){
            throw new ApiException(406, "Invalid Input Arguments");
        }

        if(strtolower($lang) != "java" && strtolower($lang) != "kotlin" && strtolower($lang) != "python"){
            throw new ApiException(406, "Invalid Input Programming Language");
        }

        try {
            $output = api::curl_post_exec("finetune", array('code_to_format' => $code, 'language' => $lang));
        } catch (\Throwable $th) {
            throw new ApiExceptionHTML(500, $th->getMessage()  );
        }
  
        return array('ok' => 1);

    }


    private static function getHTML($code, $output){
        //output was a string - need an array
        $output = json_decode($output, 1);
        if(empty($output) || $output === FALSE){
            throw new Exception("Baselearner did not return a valid json string");
        }

        $setHtmlString = "<!DOCTYPE html>
        <html>
        <style>
        .ANY {
            color: black;
            font-weight: normal;
            font-style: normal;
        }
        .KEYWORD {
            color: blue;
            font-weight: bold;
            font-style: normal;
        }
        .LITERAL {
            color: lightskyblue;
            font-weight: bold;
            font-style: normal;
        }
        .CHAR_STRING_LITERAL {
            color: darkgoldenrod;
            font-weight: normal;
            font-style: normal;
        }
        .COMMENT {
            color: grey;
            font-weight: normal;
            font-style: italic;
        }
        .CLASS_DECLARATOR {
            color: crimson;
            font-weight: bold;
            font-style: normal;
        }
        .FUNCTION_DECLARATOR {
            color: fuchsia;
            font-weight: bold;
            font-style: normal;
        }
        .VARIABLE_DECLARATOR {
            color: purple;
            font-weight: bold;
            font-style: normal;
        }
        .TYPE_IDENTIFIER {
            color: darkgreen;
            font-weight: bold;
            font-style: normal;
        }
        .FUNCTION_IDENTIFIER {
            color: dodgerblue;
            font-weight: normal;
            font-style: normal;
        }
        .FIELD_IDENTIFIER {
            color: coral;
            font-weight: normal;
            font-style: normal;
        }
        .ANNOTATION_DECLARATOR {
            color: lightslategray;
            font-weight: lighter;
            font-style: italic;
        }
        </style>";

        $hcodearray = api::getHCodeVals($output);
        $strarray = api::getStrings($code, $output);
        $full_string = $setHtmlString."<pre>";

        for ($i=0; $i < count($hcodearray); $i++) {
            $class_string = "";
            $css_class = "";
		    switch ($hcodearray[$i]) {
            case 0:
                $css_class = "ANY";
                break;
			case 1:
				$css_class = "KEYWORD";
				break;
			case 2:
				$css_class = "LITERAL";
				break;
			case 3:
				$css_class = "CHAR_STRING_LITERAL";
				break;
			case 4:
				$css_class = "COMMENT";
				break;
			case 5:
				$css_class = "CLASS_DECLARATOR";
				break;
			case 6:
				$css_class = "FUNCTION_DECLARATOR";
				break;
			case 7:
				$css_class = "VARIABLE_DECLARATOR";
				break;
			case 8:
				$css_class = "TYPE_IDENTIFIER";
				break;
			case 9:
				$css_class = "FUNCTION_IDENTIFIER";
				break;
			case 10:
				$css_class = "FIELD_IDENTIFIER";
				break;
			case 11:
				$css_class = "ANNOTATION_DECLARATOR";
				break;
		    }
            $class_string = "<code class=\"".$css_class."\">".$strarray[$i]."</code>";
            $full_string = $full_string.$class_string;
        }

        $full_string = $full_string."</pre>"."</html>";
        //print($full_string);
        return $full_string;

    }

    //This function returns the predicted hcode as an array from the $output variable
    private static function getHCodeVals($output){
        $hcodearray = array();
        if(!isset($output["prediction"])){
            throw new Exception("getHCodeVals Output is not set");
        }
        foreach ($output["prediction"] as $key => $value) {
			array_push($hcodearray, $value);
		}
        return $hcodearray;
    }

    //This function returns an array of all the strings in the $output variable
    private static function getStrings($code, $output){
        $strarray = array();
        if(!isset($output["result"])){
            throw new Exception("getStrings Output is not set");
        }
        foreach ($output["result"] as $key => $value) {
            $word = substr($code, $value["startIndex"], $value["endIndex"] - $value["startIndex"]  + 1);
			array_push($strarray, $word);
		}
        return $strarray;
    }

    private static function curl_post_exec($method, $params){

        $curl = curl_init();

        curl_setopt_array($curl, array(
          CURLOPT_URL => api::$learner_url . $method,
          CURLOPT_RETURNTRANSFER => true,
          CURLOPT_ENCODING => '',
          CURLOPT_MAXREDIRS => 10,
          CURLOPT_TIMEOUT => 0,
          CURLOPT_FOLLOWLOCATION => true,
          CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
          CURLOPT_CUSTOMREQUEST => 'POST',
          CURLOPT_POSTFIELDS => $params
        ));
        
        $output = curl_exec($curl);


        if (curl_errno($curl)) {
            $error_msg = 'CURL Error url: ' . api::$learner_url . $method . ' error:' . curl_error($curl);
            $curl_errno = curl_errno($curl);
            throw new Exception($error_msg, $curl_errno);
        }
        else{
            $curl_info = curl_getinfo($curl);
            if($curl_info['http_code'] != 200){
                $error_msg = 'CURL Error url: ' . api::$learner_url . $method . ' http_code:' . $curl_info['http_code'].  ' msg: '.  $output;
                throw new Exception($error_msg, $curl_info['http_status']);
            }
        }

        curl_close($curl);
    
    
        return $output;

        
    }
}