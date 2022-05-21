<?php


function get_secret(){
    return "hsdiwu8&%$$";
}

class Api{

    /**
     * This function returns the highlighted code. It returns either a full HTML document or a JSON
     * @param string $lang
     * @param string $code
     * @param string $secret: It is a shared secret used to prevent anauthorized use of the API
     * @param string $mode : Accepts html or JSON
     * @return array
     * @throws ApiException if the arguments are empty or non valid
     * @throws ApiExceptionHTML if the predict endpoint curl_post fails or the html format failed
     */
    public static function highlight($lang = '', $code = '', $secret = '', $mode = 'html'){

        if(empty($mode)){
            $mode = 'html';
        }

        if(empty($lang) || empty($code)){
            Logger::log("Empty code or lang " , Logger::ERROR);
            throw new ApiException(406, "Invalid Input Arguments");
        }

        if(strtolower($lang) != "java" && strtolower($lang) != "kotlin" && strtolower($lang) != "python"){
            Logger::log("Invalid Input Programming Language. Input was: " .$lang, Logger::ERROR);
            throw new ApiException(406, "Invalid Input Programming Language");
        }

        if ( base64_encode(base64_decode($code, true)) !== $code){
            Logger::log("The code field must be base64 encoded. Input was: " .$code, Logger::ERROR);
            throw new ApiException(406, "The code field must be base64 encoded ");
        }

        if($mode != "html" && $mode != "json"){
            Logger::log("The input parameter mode can only be json or html " .$mode, Logger::ERROR);
            throw new ApiException(406, "The input parameter mode can only be json or html ");
        }

        if($secret != get_secret()){
            Logger::log("Anauthorized use of the API. Wrong secret. Input was: " .$secret, Logger::ERROR);
            throw new ApiException(401, "Anauthorized use of the API. Wrong secret");
        }

        Logger::log("Input for prediction. Language: " . $lang ." \nInput:\n". substr(base64_decode($code, true), 0, 20) . "..."  , Logger::INFO);

        if(Api::decide_if_predict()){
            Logger::log("Input chosen for finetuning", Logger::INFO);
            try {
                $output = Api::curl_post_exec("finetune", array('code_to_format' => $code, 'language' => strtolower($lang)));
                //print( $output);
            } catch (\Throwable $th) {
                Logger::log("Finetune inside predict threw exception. Exception Message" .$th->getMessage(), Logger::ERROR);
                throw new ApiExceptionHTML(500, $th->getMessage()  );
            }
        }


        try {
            $output = Api::curl_post_exec("predict", array('code_to_format' => $code, 'language' =>  strtolower($lang)));
        } catch (\Throwable $th) {
            Logger::log("Predict threw exception. Exception Message" .$th->getMessage(), Logger::ERROR);
            throw new ApiExceptionHTML(500, $th->getMessage()  );
        }


        try {
            if($mode == "html"){
                $full_HTML = Api::getHTML(base64_decode($code), $output);
                return array('resp' => base64_encode($full_HTML));
            }
            else{
                $json_array = Api::getJSON(base64_decode($code), $output);
                return $json_array;
            }
        } catch (\Throwable $th) {
            Logger::log("api::getHTML threw exception. Exception Message" .$th->getMessage(), Logger::ERROR);
            throw new ApiException(500, "api::getHTML error. Log: ". $th->getMessage());
        }

    }


    /**
     * It uses the finetune function of the model
     * @param string $lang
     * @param string $code
     * @param string $secret: It is a shared secret used to prevent anauthorized use of the API
     * @return array
     * @throws ApiException if the arguments are empty or non valid
     * @throws ApiExceptionHTML if the finetune endpoint curl_post fails
     */
    public static function finetune($lang = '', $code = '', $secret = ''){

        if(empty($lang) || empty($code)){
            Logger::log("Empty code or lang " , Logger::ERROR);
            throw new ApiException(406, "Invalid Input Arguments");
        }

        if(strtolower($lang) != "java" && strtolower($lang) != "kotlin" && strtolower($lang) != "python"){
            Logger::log("Invalid Input Programming Language. Input was: " .$lang, Logger::ERROR);
            throw new ApiException(406, "Invalid Input Programming Language");
        }

        if ( base64_encode(base64_decode($code, true)) !== $code){
            Logger::log("The code field must be base64 encoded. Input was: " .$code, Logger::ERROR);
            throw new ApiException(406, "The code field must be base64 encoded ");
        }

        if($secret != get_secret()){
            Logger::log("Anauthorized use of the API. Wrong secret. Input was: " .$secret, Logger::ERROR);
            throw new ApiException(401, "Anauthorized use of the API. Wrong secret");
        }
        Logger::log("Input for finetuninf. Language: " . $lang ." \nInput:\n". substr(base64_decode($code, true), 0, 20) . "..."  , Logger::INFO);
        try {
            $output = Api::curl_post_exec("finetune", array('code_to_format' => $code, 'language' => strtolower($lang)));
        } catch (\Throwable $th) {
            throw new ApiExceptionHTML(500, $th->getMessage()  );
        }

        return array('ok' => 1);

    }

    /**
     * Returns the whole <html> formated code
     * @param mixed $code
     * @param mixed $output
     * @return string
     * @throws Exception if the output is not well formatted
     */
    private static function getHTML($code, $output){
        //output was a string - need an array
        $output = json_decode($output, 1);
        if(empty($output) || $output === FALSE){
            throw new Exception("Baselearner did not return a valid json string");
        }

        $setHtmlString = "<!DOCTYPE html>
        <html>
        <style>
        .GENERAL {
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
        $full_string = $setHtmlString."<pre>";

        $hcodearray = Api::getHCodeVals($output);
        $strarray = Api::getStrings($code, $output);


        $class_string_arr = Api::format_html_code_strings($hcodearray,  $strarray);

        // for ($i=0; $i < sizeof($hcodearray); $i++) {
        //     echo $hcodearray[$i] . ": " . $strarray[$i] . "code: " . $class_string_arr[$i]."\n";
        // }

        $full_string .=  Api::format_html_code($class_string_arr, $output, $code);

        $full_string = $full_string."</pre>"."</html>";
        //print($full_string);
        return $full_string;

    }
    private static function getJSON($code, $output){
        //output was a string - need an array
        $output = json_decode($output, 1);
        if(empty($output) || $output === FALSE){
            throw new Exception("Baselearner did not return a valid json string");
        }

        if(!isset($output["result"])){
            throw new Exception("getStrings Output is not set");
        }

        $result_array = array();

        $words = Api::getStrings($code, $output);
        $hcodearray = Api::getHCodeVals($output);

        foreach ($output["result"] as $key => $value) {

            $type = Api::getType($hcodearray[$key]);

            $word = array(
                'startIndex' => $value["startIndex"],
                'endIndex' => $value["endIndex"],
                'type' => $type,
                'token' => $words[$key]
            );

            array_push($result_array, $word);
		}

        return $result_array;

    }
    /**
     * This function returns the predicted hcode as an array from the $output variable
     * @param mixed $output
     * @return array
     * @throws Exception if the output is not well formatted
     */
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

    /**
     * Formats the HTML code replacing with <code></code> elements the highlighted code.
     * @param mixed $class_string_arr
     * @param mixed $output
     * @param mixed $code
     * @return string
     * @throws Exception if the output is not well formatted
     */
    private static function format_html_code($class_string_arr, $output, $code){

        if(!isset($output["result"])){
            throw new Exception("getStrings Output is not set.");
        }
        $end_of_last_token = -1;
        $all_code_in_strings = array();
        $i = 0;
        foreach ($output["result"] as $key => $value) {
            if($value["startIndex"] - ($end_of_last_token + 1)  > 0 ){

                $characters_in_between = mb_substr($code, $end_of_last_token + 1,   $value["startIndex"] - ($end_of_last_token + 1) , "UTF-8");
                $characters_in_between = Api::format_special_chars_to_html($characters_in_between);
                array_push($all_code_in_strings, $characters_in_between);

                // echo "startIndex: ". $value["startIndex"] ."\n";
                // echo "endIndex: ". $value["endIndex"] ."\n";
                // echo "end_of_last_token: ". $end_of_last_token ."\n";
                // echo $characters_in_between ."\n";
                // echo "=========\n";

            }

            $code_string = $class_string_arr[$i++];
            array_push($all_code_in_strings, $code_string);
            $end_of_last_token = $value["endIndex"];
        }

        $code = implode("", $all_code_in_strings);
        // echo print_r($all_code_in_strings, 1);
        // echo  $code;
        return $code;
    }


    /**
     * Returns the array of <code class="{class}"></code> elememts where class is decided by the hcodearray value
     * @param mixed $hcodearray
     * @param mixed $strarray
     * @return array
     */
    private static function format_html_code_strings($hcodearray, $strarray){

        $class_string_arr = array();
        for ($i=0; $i < count($hcodearray); $i++) {
            $class_string = "";
            $css_class = Api::getType($hcodearray[$i]);

            // $tt = str_split($strarray[$i]);
            // echo $strarray[$i];
            // foreach ($tt as  $ss) {
            //     echo 'char: ' .mb_ord($ss) . "\n";
            // }
            // echo $hcodearray[$i] . $strarray[$i] ."\n";
            $class_string = "<code class=\"".$css_class."\">".Api::format_special_chars_to_html($strarray[$i])."</code>";
            $class_string_arr[] = $class_string;
        }
        return $class_string_arr;
    }

    private static function getType($hcodevalue){
        switch ($hcodevalue) {
            case 0:
                $type = "GENERAL";
                break;
            case 1:
                $type = "KEYWORD";
                break;
            case 2:
                $type = "LITERAL";
                break;
            case 3:
                $type = "CHAR_STRING_LITERAL";
                break;
            case 4:
                $type = "COMMENT";
                break;
            case 5:
                $type = "CLASS_DECLARATOR";
                break;
            case 6:
                $type = "FUNCTION_DECLARATOR";
                break;
            case 7:
                $type = "VARIABLE_DECLARATOR";
                break;
            case 8:
                $type = "TYPE_IDENTIFIER";
                break;
            case 9:
                $type = "FUNCTION_IDENTIFIER";
                break;
            case 10:
                $type = "FIELD_IDENTIFIER";
                break;
            case 11:
                $type = "ANNOTATION_DECLARATOR";
                break;
            default:
                $type = "UNKONOWN";
                break;
        }
        return $type;
    }

    /**
     * Returns an array of all the substrings in the code from startIndex to endIndex as extracted by the response of the highlight (outout)
     * @param mixed $code
     * @param mixed $output
     * @return array
     * @throws Exception if the output is not well formatted
     */
    private static function getStrings($code, $output){
        $strarray = array();
        if(!isset($output["result"])){
            throw new Exception("getStrings Output is not set");
        }
        foreach ($output["result"] as $key => $value) {

            $word = substr($code, $value["startIndex"], $value["endIndex"] - $value["startIndex"]  + 1);
            //echo "startIndex: " .$value["startIndex"].  "endIndex: ". $value["endIndex"] . " word: ".  $word ."\n";
			array_push($strarray, $word);
		}
        return $strarray;
    }

    /**
     * Replaces new line with a <br>
     * It is a function in case we need to made other replaces as well.
     * @param mixed $string
     * @return string
     */
    private static function format_special_chars_to_html($string){
        $string = str_replace(' ', '&nbsp;', $string);
        $string = nl2br($string);
        return $string;
    }

    /**
     * This method executes a curl post
     * @param mixed $method
     * @param mixed $params
     * @return string|bool the response of curl_exec
     * @throws Exception if curl is executed with an error or whether the http_status returned was not 200
     */
    private static function curl_post_exec($method, $params){

        $curl = curl_init();

        curl_setopt_array($curl, array(
          CURLOPT_URL => Api::get_learner_url() . $method,
          CURLOPT_RETURNTRANSFER => true,
          CURLOPT_ENCODING => '',
          CURLOPT_MAXREDIRS => 10,
          CURLOPT_TIMEOUT => 0,
          CURLOPT_FOLLOWLOCATION => true,
          CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
          CURLOPT_CUSTOMREQUEST => 'POST',
          CURLOPT_POSTFIELDS => $params,
          CURLOPT_SSL_VERIFYPEER => false
        ));

        $output = curl_exec($curl);


        if (curl_errno($curl)) {
            $error_msg = 'CURL Error url: ' . Api::get_learner_url() . $method . ' error:' . curl_error($curl);
            $curl_errno = curl_errno($curl);
            throw new Exception($error_msg, $curl_errno);
        }
        else{
            $curl_info = curl_getinfo($curl);
            if($curl_info['http_code'] != 200){
                $error_msg = 'CURL Error url: ' . Api::get_learner_url() . $method . ' http_code:' . $curl_info['http_code'].  ' msg: '.  $output;
                throw new Exception($error_msg, $curl_info['http_status']);
            }
        }

        curl_close($curl);
        return $output;


    }

    /**
     * This function exists in case we need to decide which input should be sent for prediction. At the moment it returns always true
     * @return bool
     */
    private static function decide_if_predict(){
        return true;
    }

    /**
     * Define the learner's URL
     * @return string
     */
    private static function get_learner_url(){

        if($_SERVER['SERVER_NAME'] == "host.docker.internal" || $_SERVER['SERVER_NAME'] == "localhost" || $_SERVER['SERVER_NAME'] == "127.0.0.1" || $_SERVER['SERVER_NAME'] == ""){
            return "http://learner:9007/";
        }
        else{
            return "http://ase-service-1.service.local:9007/";
        }
    }
}