# End-to-end testing

The e2e microservice tests the application flow from beginning to end,
validating the functionalities provided to the user.

## Technology and components

The e2e container uses the Cypress framework for end-to-end testing and consists
of the following main components:

### The tests: cypress/integration/e2e.spec.js

Tests the system from src_react to src_php to src_learner and back.

### Configuration: cypress.json

Contains necessary information for testing: the application URL and API URL.

### Debugging: cypress/screenshots, cypress/videos

Screenshots and videos are saved here for debugging failed runs.

## To run

Run this command in the parent src/ directory:

docker-compose -f docker-compose-test-e2e.yml up
