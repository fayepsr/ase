<?php

use PHPUnit\Framework\TestCase;

final class ApiUnitTest extends TestCase
{
    public function test(): void
    {
        $this->assertEquals(1, 1);
    }


    public function testGetStringsEmptyInputThrowsException()
    {

        $throwsException = false;
        try {
            $foo = self::getMethod('getStrings');
            $foo->invokeArgs(null, array('', array()));
        } catch (\Throwable $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);
    }

    public function testGetStringsEmptyCodeWithGivenSecondParamRturnsEmptyArray()
    {

        try {
            $foo = self::getMethod('getStrings');
            $result = $foo->invokeArgs(null, array('', array("result")));
        } catch (\Throwable $th)
         {
        }
        $this->assertEmpty( $result);
    }

    public function testGetStringsSingleString()
    {

        try {
            $foo = self::getMethod('getStrings');
            $result = $foo->invokeArgs(null, array('test', array("result" => array(array("startIndex" => 0, "endIndex" => 3 )))));
        } catch (\Throwable $th)
         {
        }
        $this->assertEquals($result,array("test") );
    }

    public function testGetStringsMultipleStrings()
    {

        try {
            $foo = self::getMethod('getStrings');
            $result = $foo->invokeArgs(null, array('test 55', array("result" => array(array("startIndex" => 0, "endIndex" => 3 ), array("startIndex" => 5, "endIndex" => 7 )))));
        } catch (\Throwable $th)
         {
        }
        $this->assertEquals($result,array("test", "55") );
    }

    public function test_format_html_code_EmptyInputThrowsException()
    {

        $throwsException = false;
        try {
            $foo = self::getMethod('format_html_code');
            $foo->invokeArgs(null, array('', array()));
        } catch (\Throwable $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);
    }


    public function testformat_html_code_simple_example()
    {

        
        try {
            $foo = self::getMethod('format_html_code');
            $result = $foo->invokeArgs(
                null, 
                array(
                    array("<code class=\"UNKNOWN\">test</code>", "<code class=\"UNKNOWN\">55</code>"), 
                    array("result" => array(array("startIndex" => 0, "endIndex" => 3 ), array("startIndex" => 5, "endIndex" => 7 ))),
                    "test 55"
                ));
        } catch (\Throwable $th)
         {
        }
        $this->assertEquals($result, '<code class="UNKNOWN">test</code>&nbsp;<code class="UNKNOWN">55</code>' );
    }

    public function test_getHCodeVals_EmptyInputThrowsException()
    {
        $throwsException = false;
        try {
            $foo = self::getMethod('getHCodeVals');
            $foo->invokeArgs(null, array('', array()));
        } catch (\Throwable $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);
    }

    public function test_getHCodeVals_EmptyArrayReturnsEmptyArray()
    {
        try {
            $foo = self::getMethod('getHCodeVals');
            $result = $foo->invokeArgs(null, array(array("prediction" => array())));
        } catch (\Throwable $th)
         {
        }
        $this->assertEquals($result, array());
    }

    public function test_getHCodeVals_SimpleExample()
    {
        try {
            $foo = self::getMethod('getHCodeVals');
            $result = $foo->invokeArgs(null, array(array("prediction" => array("tt"))));
        } catch (\Throwable $th)
         {
        }
        $this->assertEquals($result, array("tt"));
    }

    public function test_highlight_non_accepted_language_throws_exception()
    {
        $throwsException = false;
        try {
            $foo = self::getMethod('highlight');
             $foo->invokeArgs(null, array("tt", "tt"));
        } catch (Exception $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);

    }

    public function test_highlight_non_accepted_mode_throws_exception()
    {
        $throwsException = false;
        try {
            $foo = self::getMethod('highlight');
            $result = $foo->invokeArgs(null, array("python", "cHJpbnQoJzU1Jyk=", get_secret(), "wrong_mode"));
        } catch (Exception $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);

    }


    public function test_highlight_empty_code_throws_exception()
    {
        $throwsException = false;
        try {
            $foo = self::getMethod('highlight');
            $foo->invokeArgs(null, array("python", ""));
        } catch (Exception $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);
    }

    public function test_highlight_nonbase64encoded_code_throws_exception()
    {
        $throwsException = false;
        try {
            $foo = self::getMethod('highlight');
            $foo->invokeArgs(null, array("python", "tt"));
        } catch (Exception $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);
    }
    
    public function test_highlight_valid_example_returnswellbase64encodedresult()
    {
       
        try {
            $foo = self::getMethod('highlight');
            $result = $foo->invokeArgs(null, array("python", "cHJpbnQoJzU1Jyk=", get_secret()));
        } catch (Exception $th)
         {
        }
     
        $this->assertEquals(  base64_encode(base64_decode($result, true)), $result );
    }
    
    
    public function test_finetune_non_accepted_language_throws_exception()
    {
        $throwsException = false;
        try {
            $foo = self::getMethod('finetune');
            $foo->invokeArgs(null, array("tt", "tt"));
        } catch (Exception $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);

    }

    public function test_finetune_empty_code_throws_exception()
    {
        $throwsException = false;
        try {
            $foo = self::getMethod('finetune');
            $foo->invokeArgs(null, array("python", ""));
        } catch (Exception $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);
    }

    public function test_finetune_nonbase64encoded_code_throws_exception()
    {
        $throwsException = false;
        try {
            $foo = self::getMethod('finetune');
            $foo->invokeArgs(null, array("python", "tt"));
        } catch (Exception $th)
         {
            $throwsException = true;
        }
        $this->assertTrue( $throwsException);
    }
   
    public function test_getJSON(){

        $config  = require_once("/tests/tests/predict_correct_output.php");
        $foo = self::getMethod('getJSON');
        $result = $foo->invokeArgs(null, array(base64_decode($config["input"]["code_to_format"]), $config["output"]));
        $this->assertIsArray($result);
    } 

    protected static function getMethod($name)
    {
        $class = new ReflectionClass('Api');
        $method = $class->getMethod($name);
        $method->setAccessible(true);
        return $method;
    }


}
