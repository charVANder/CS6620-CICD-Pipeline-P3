#!/bin/bash
echo "----------Starting the Pokemon API stack...----------"
echo "This will run until manually stopped (Ctrl+C)"
docker-compose -f docker/docker_compose_stack.yml up --build
echo "Cleaning up..."
docker-compose -f docker/docker_compose_stack.yml down
