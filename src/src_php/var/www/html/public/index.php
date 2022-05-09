<?php
	header('Access-Control-Allow-Origin: *');
	header('Content-Type: application/json; charset=utf-8');

	require_once('../classes/classes.php');

    $args = $_GET['args'];
	$uri = explode('/',$args); //api/v1/highlight

	try {	
		switch ($uri[2]) {
			case 'highlight':
				$response = api::highlight($_POST['lang'], $_POST['code'], $_POST['secret']);
				break;
			case 'finetune':
				$response = api::finetune($_POST['lang'], $_POST['code'],  $_POST['secret']);
				break;
			case 'app_health':
				$response ='ok';
				break;					
			default:
				Logger::log("Unknown URI requested. URI: " .$args, Logger::ERROR);
				throw new ApiException(404, 'The request was not found');
		}	
	
		echo json_encode($response);
		
	} catch (ApiException $ex) {
			//TODO : Porbably write error log
	}
	catch (ApiExceptionHTML $ex ){
		
	}
	

	