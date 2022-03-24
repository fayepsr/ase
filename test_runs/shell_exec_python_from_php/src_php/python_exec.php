<?php 

$command = escapeshellcmd('python2.7 /home/python_example/test.py');
$output = shell_exec($command);
echo $output;

?>