import pytest
import requests
import os
import time

API_URL = os.getenv('API_URL', 'http://localhost:5000')

@pytest.fixture(scope="session", autouse=True)
def wait_for_api():
    '''ADDED THIS AT THE END BECAUSE MY TESTS KEPT FAILING TT_TT
    '''
    for blah in range(30):
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code == 200:
                print("API is healthy.")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
    raise RuntimeError("API not ready after 30 attempts")

@pytest.fixture
def sample_pokemon():
    '''A simple sample pokemon for tests. Yes, Absol is one of my favorite Pokemon.
    '''
    return {
        "id": 359,
        "name": "Absol",
        "level": 25,
        "type": "Dark",
        "hp": 100,
        "max_hp": 100
    }

@pytest.fixture
def cleanup_pokemon():
    '''Keeping track of deleted pokemon and deleting them after tests
    '''
    created_ids = []
    def add_id(pokemon_id):
        created_ids.append(pokemon_id)
    yield add_id

    for pokemon_id in created_ids:
        try:
            requests.delete(f"{API_URL}/pokemon/{pokemon_id}")
        except Exception:
            pass