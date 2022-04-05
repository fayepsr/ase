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

        //Calling the function to get the full HTML string
        $full_HTML = api::getHTML($code, $output);
        
        return array('resp' => "Formatted Input");

    }

    private static function getHTML($code, $output){
        //output was a string - need an array
        $output = json_decode($output, 1);
        $hcodearray = api::getHCodeVals($output);
        $strarray = api::getStrings($code, $output);
        $full_string = "<pre>";

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

        $full_string = $full_string."</pre";
        print($full_string);
        return $full_string;

    }

    //This function returns the predicted hcode as an array from the $output variable
    private static function getHCodeVals($output){
        $hcodearray = array();
        foreach ($output["prediction"] as $key => $value) {
			array_push($hcodearray, $value);
		}
        return $hcodearray;
    }

    //This function returns an array of all the strings in the $output variable
    private static function getStrings($code, $output){
        $strarray = array();
        foreach ($output["result"] as $key => $value) {
            $word = substr($code, $value["startIndex"], $value["endIndex"] - $value["startIndex"]  + 1);
			array_push($strarray, $word);
		}
        return $strarray;
    }
}