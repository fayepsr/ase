<?php
	header('Content-Type: application/json; charset=utf-8');

	require_once('../classes/classes.php');

    $args = $_GET['args'];
	$uri = explode('/',$args); //api/v1/highlight


	try {	
		switch ($uri[2]) {
			case 'highlight':
				$response = api::highlight($_POST['lang'], $_POST['code']);
				break;
			default:
				throw new ApiException(404, 'The request was not found');
		}	
	
		echo json_encode($response);
		
	} catch (ApiException $ex) {
			//TODO : Porbably write error log
	}
	

	