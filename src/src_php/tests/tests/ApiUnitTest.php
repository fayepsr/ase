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
        $this->assertEquals($result, '<code class="UNKNOWN">test</code> <code class="UNKNOWN">55</code>' );
    }


    protected static function getMethod($name)
    {
        $class = new ReflectionClass('api');
        $method = $class->getMethod($name);
        $method->setAccessible(true);
        return $method;
    }
}
