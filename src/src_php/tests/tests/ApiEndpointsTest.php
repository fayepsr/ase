<?php 

use PHPUnit\Framework\TestCase;

final class ApiEndpointsTest  extends TestCase{

    public function testWrongURL(): void
    {
        $exception_thrown = false;
        try {
            require_once("../var/www/html/public/index.php");
        } catch (\Throwable $th) {
            $exception_thrown = true;
        }
        $this->assertTrue($exception_thrown);
    }

    public function testHighlightURL(): void
    {
        $exception_thrown = false;
        try {
            $_GET['args'] = "/api/v1/highlight";
            require_once("../var/www/html/public/index.php");
        } catch (Exception $th) {
            $exception_thrown = true;
            echo "Thrown".$th;
            print($th->getMessage());
        }
        $this->assertFalse($exception_thrown);
    }

    public function testFinetuneURL(): void
    {
        $exception_thrown = false;
        try {
            $_GET['args'] = "/api/v1/finetune";
            require_once("../var/www/html/public/index.php");
        } catch (Exception $th) {
            $exception_thrown = true;
            echo "Thrown".$th;
            print($th->getMessage());
        }
        $this->assertFalse($exception_thrown);
    }    
}
