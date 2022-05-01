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



    protected static function getMethod($name)
    {
        $class = new ReflectionClass('api');
        $method = $class->getMethod($name);
        $method->setAccessible(true);
        return $method;
    }
}
