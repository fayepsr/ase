<?php 

function src_autoloader($class) {
    include '/var/www/html/classes/'.$class.'.class.php';

}
   
spl_autoload_register('src_autoloader');