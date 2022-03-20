<?php 

$command = escapeshellcmd('javac -d /home/java_example/ /home/java_example/HelloWorld.java');
$output = shell_exec($command);
echo $output;

$command = escapeshellcmd('java -classpath /home/java_example/ HelloWorld');
$output = shell_exec($command);
echo $output;


?>