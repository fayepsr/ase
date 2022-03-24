<?php 

$command = escapeshellcmd('python3.9 /home/src_python/shmodel.py');
$output = shell_exec($command);
echo $output;
