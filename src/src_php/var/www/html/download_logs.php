<?php


    if($_GET['secret'] != "52r7$%^Gjj38"){
        return;
    }

    
    $zipname = 'logs.zip';
    $zip = new ZipArchive;
    if($zip->open($zipname, ZipArchive::CREATE)){
        foreach (glob("/var/www/html/tmp/*.txt") as $file) { 
            $tt = $zip->addFile($file, basename($file));
        }
        $zip->close();

        header('Content-Type: application/zip');
        header("Content-Disposition: attachment; filename = " .basename($zipname));
        header('Content-Length: ' . filesize($zipname));
        flush();
        readfile($zipname);
        // delete file
        unlink($zipname);

   } else {
       echo 'Failed to download logs';
   }