#!/bin/bash
echo "----------Running the Pokemon API tests...----------"
docker-compose -f docker/docker_compose_test.yml up --build --abort-on-container-exit
exit_code=$?
echo "Cleaning up test environment..."
docker-compose -f docker/docker_compose_test.yml down
if [ $exit_code -eq 0 ]; then
    echo "All tests have passed! Exit code: 0"
    exit 0
else
    echo "Testing has failed! Exit code: non-zero"
    exit 1
fi
