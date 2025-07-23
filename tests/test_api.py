import pytest
import requests
import json
import os

API_URL = os.getenv("API_URL", "http://localhost:5000")

## Sending a GET requests with appropriate parameters returns expected JSON from the database
def test_get_pokemon_with_appropriate_parameters(sample_pokemon, cleanup_pokemon):
    # Creating
    response = requests.post(f"{API_URL}/pokemon", json=sample_pokemon)
    assert response.status_code == 201
    cleanup_pokemon(sample_pokemon['id'])

    # Testing GET w/ ID
    response = requests.get(f"{API_URL}/pokemon?id={sample_pokemon['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == sample_pokemon['name']
    assert data['type'] == sample_pokemon['type']
    assert int(data['level']) == sample_pokemon['level']


## Sending a GET request that finds no results returns the appropriate response
def test_get_pokemon_no_results():
    response = requests.get(f"{API_URL}/pokemon?id=9999")
    assert response.status_code == 404
    assert "Error" in response.json()


## Sending a GET request with no parameters returns the appropriate response
def test_get_pokemon_no_params():
    response = requests.get(f"{API_URL}/pokemon")
    assert response.status_code == 200
    data = response.json()
    assert "pokemon" in data
    assert 'count' in data
    assert isinstance(data['pokemon'], list)


## Sending a GET request with incorrect parameters returns the appropriate response
def test_get_pokemon_incorrect_parameters():
    response = requests.get(f"{API_URL}/pokemon?id=blahblahblahTHISISINCORRECT")
    assert response.status_code == 400
    assert 'Error' in response.json()


## Sending a POST request results in the JSON body being stored as an item in the database, and an object in an S3 bucket
def test_post_pokemon_stores_in_database_and_s3(cleanup_pokemon):
    pokemon_data = {
        "id": 133,
        "name": "Eevee",
        "level": 25,
        "type": "Normal",
        "hp": 100,
        "max_hp": 180,
    }
    response = requests.post(f"{API_URL}/pokemon", json=pokemon_data)
    assert response.status_code == 201
    cleanup_pokemon(pokemon_data['id'])

    # Retrieve and see if it's there properly
    get_response = requests.get(f"{API_URL}/pokemon?id={pokemon_data['id']}")
    assert get_response.status_code == 200
    stored_data = get_response.json()
    assert stored_data['name'] == pokemon_data['name']
    assert stored_data['level'] == pokemon_data['level']


## Sending a duplicate POST request returns the appropriate response
def test_post_duplicate_pokemon(sample_pokemon, cleanup_pokemon):
    response = requests.post(f"{API_URL}/pokemon", json=sample_pokemon)
    assert response.status_code == 201

    # Trying to create a duplicate
    duplicate_response = requests.post(f"{API_URL}/pokemon", json=sample_pokemon)
    assert duplicate_response.status_code == 409
    cleanup_pokemon(sample_pokemon['id'])


## Sending a PUT request that targets an existing resource results in updates to the appropriate item in the database and object in the S3 bucket
def test_put_existing_pokemon_updates_database_and_s3(sample_pokemon, cleanup_pokemon):
    # Creating pokemon
    response = requests.post(f"{API_URL}/pokemon", json=sample_pokemon)
    assert response.status_code == 201
    cleanup_pokemon(sample_pokemon['id'])

    # Updating pokemon
    updated_data = {
        "name": "Zoroark",
        "level": 30,
        "type": "Dark",
        "hp": 120,
        "max_hp": 120
    }
    put_response = requests.put(f"{API_URL}/pokemon/{sample_pokemon['id']}", json=updated_data)
    assert put_response.status_code == 200

    # Does it update correctly?
    get_response = requests.get(f"{API_URL}/pokemon?id={sample_pokemon['id']}")
    data = get_response.json()
    assert data["name"] == "Zoroark"
    assert data["level"] == 30
    cleanup_pokemon(sample_pokemon["id"])


## Sending a PUT request with no valid target returns the appropriate response
def test_put_no_valid_target():
    pokemon_data = {
        "name": "MissingNo",
        "level": 50,
        "type": "ThisIsAGlitch"
    }
    response = requests.put(f"{API_URL}/pokemon/9999", json=pokemon_data)
    assert response.status_code == 404
    assert 'Error' in response.json()


## Sending a DELETE request results in the appropriate item being removed from the database and object being removed from the S3 bucket
def test_delete_pokemon_removes_from_database_and_s3(sample_pokemon):
    response = requests.post(f"{API_URL}/pokemon", json=sample_pokemon)
    assert response.status_code == 201

    delete_response = requests.delete(f"{API_URL}/pokemon/{sample_pokemon['id']}")
    assert delete_response.status_code == 200

    get_response = requests.get(f"{API_URL}/pokemon?id={sample_pokemon['id']}")
    assert get_response.status_code == 404


## Sending a DELETE request with no valid target returns the appropriate response
def test_delete_no_valid_target():
    response = requests.delete(f"{API_URL}/pokemon/9999")
    assert response.status_code == 404
    assert "Error" in response.json()
