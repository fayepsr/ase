# Frontend container

The React microservice provides a simple frontend application for testing and
demonstrating the capabilities of our syntax highlighting service.

## Technology and components

This microservice uses the React library for building the user interface and
contains the following main components:

### The application: app/src

Contains the React components in JavaScript and their corresponding css files.
Form.js handles the core functionalities of the frontend and sends POST requests
to our web service via the PHP API contained in src_php.

### Environment variables: app/.env

Contains necessary information for accessing the web service. By default, the
frontend service will send requests to the deployed version of our service on
Lightsail.

### Dockerfile

Builds the image from a node base and installs the necessary dependencies before
running the service. The URL of our web service API is set to its URL within the
Docker network. This ensures that using the React application in Docker will
send requests to the Docker version of our service.

## Core Functionalities

- Input: Code language selection (Java, Kotlin, or Python)
- Input: Textual input of code
- Input: Output format selection (HTML or JSON)
- Submit -- formats and sends request to the API
- Output: Displays the highlighted result (in HTML or JSON)
- Output: Displays error if there is one

## Tests

The unit tests are located in app/src/App.test.js. They utilize the React
testing library and mock the service API.

To run, navigate to the app/ folder and run: npm test

## Run the Microservice

There are three ways to run the React application.

### Via Docker:

Run with the other microservices on Docker by navigating to the parent src/
directory and running the command: ./build_and_run_all.bat

Then access the application locally from http://localhost:3007/

### Via Local Machine:

Navigate to the app/ folder and run: npm start

This should start up the application on http://localhost:3000/

### Via the Cloud:

The deployed version on Lightsail can be accessed from
https://container-service-2.iugkfeabdb168.eu-central-1.cs.amazonlightsail.com/
