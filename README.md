# CS6620-CICD-Pipeline-p3
This is a HW assignment for CS6620 (Cloud Computing) at the Roux Institute at Northeastern. It is a simple Pokemon-themed cloud RestAPI (with GET, PUT, POST, and DELETE endpoints) built on top of the original Pokemon class from the Part 2 assignment found [here](https://github.com/charVANder/CS6620-CICD-Pipeline-p2) (Part 1 can be found [here](https://github.com/charVANder/CS6620-CICD-Pipeline-p1)). Demonstrates test-driven development, Docker container orchestration, CRUD operations, and CI/CD workflows. For the sake of addressing the current assignment with simplicity, the previous battle mechanics were removed, focusing on turning the API into a viable cloud architecture implementation. CRUD operations were added to function in a DynamoDB table and an S3 bucket. Localstack was used to run a mock of AWS as part of the application stack. Two docker compose files with corresponding shell scripts were created to run the stack (until manually stopped) and run the tests.

## TODO (for Van while working)
* Remove the battle mechanics endpoints stuff from api.py (only simple GET/POST/PUT/DELETE will be needed)
* Remove the old Dockerfiles - I'll probably just make a single simple Dockerfile to go with the compose files.
* Change the requirements.txt and environment.yml to have boto3
* Make a simple Dockerfile
* Make an aws.py for the new aws integration stuff (like initiating the DynamoDB operations and s3 bucket stuff). I'll probably have create_pokemon, get_pokemon, get_all_pokemon, update_pokemon, and delete_pokemon all in the DB and S3.
* Create the docker-compose files (one for the stack and one for the tests).
* Fix pokemon.py so that it works with dynamoDB.
* Fix api.py so that it works with all the AWS stuff and doesn't use all the battle mechanic endpoints.
* Replace run_api.sh with run_stack.sh to work with docker-compose.yml. Similarly, update the run_tests.sh so that it works with the test docker-compose file.
* Remove test_pokemon.py and create a new file for testing configurations (need to look into if I'll need this)
  * It would be helpful to have something cleanup the pokemon after tests. Also a sample pokemon.
* Fix test_api.py so that it covers the required tests. Requirements were...
  * GET with appropriate params (testing get pokemon with id)
  * GET that finds no results (testing get pokemon not found)
  * GET with no params (testing get all pokemon)
  * GET with incorrect params (so like an invalid id)
  * POST stores in DB and S3
  * Handling duplicate POST (posting duplicate pokemon)
  * PUT updates existing resource (pokemon needs to show up in db and s3)
  * PUT with no valid target (put a non-existing pokemon)
  * DELETE removes from db and S3 (delete a pokemon and check)
  * DELETE with no valid target (delete a nonexistent pokemon)
  * Update the Github workflows
  * Fix the README

  ## References and AI Appendix
  * tbd