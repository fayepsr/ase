<?php 

// $command = escapeshellcmd('javac -d /home/src_java/ -cp /home/src_java/SHOracle.jar /home/src_java/Main.java');
// $output = shell_exec($command);
// echo $output;

$command = escapeshellcmd('java -cp /home/src_java/SHOracle.jar /home/src_java/Main.java');
$output = shell_exec($command);
echo $output;


?>