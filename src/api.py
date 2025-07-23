'''This file has been fixed since the last assignment so that it works with all the AWS stuff and doesn't use all the battle mechanic endpoints.
'''
from flask import Flask, jsonify, request
import sys
import os
from aws import PokemonAWS

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_app():
    app = Flask(__name__)
    aws = PokemonAWS()

    def validate_pkmn_data(data):
        required_stuff = ["id", "name", "level"]
        for stuff in required_stuff:
            if stuff not in data:
                return False, f"Missing {stuff}"
        if not isinstance(data["name"], str) or len(data["name"].strip()) == 0:
            return False, "Name needs to be a non-empty string"
        if not isinstance(data["level"], int) or data["level"] < 1 or data["level"] > 100:
            return False, "Level needs to be between 1 and 100"
        if not isinstance(data["id"], int) or data["id"] < 1:
            return False, "ID needs to be a positive integer"
        return True, ""
    
    ## Routes
    @app.route("/health", methods=["GET"])
    def check_health():
        return jsonify({"Status": "healthy", "Note": "The Pokemon API is running"}), 200
    
    @app.route("/pokemon", methods=["GET"])
    def get_pokemon():
        '''
        I'm combining the by_id and all_pkmn stuff together so that it's all in one place here.
        Why? Because I'm lazy :p
        '''
        pokemon_id = request.args.get('id')
        if pokemon_id:
            try: # getting specific pkmn by id
                pokemon_id = int(pokemon_id)
                pokemon_data = aws.get_pokemon(pokemon_id)
                if pokemon_data:
                    return jsonify(pokemon_data), 200
                else:
                    return jsonify({"Error": f"Pokemon with ID {pokemon_id} was not found"}), 404
            except ValueError:
                return jsonify({"Error": "Invalid Pokemon ID parameter"}), 400
        else:
            all_pokemon = aws.get_all_pokemon()
            return jsonify({"pokemon": all_pokemon, "count": len(all_pokemon)}), 200
        
    @app.route("/pokemon/<int:pokemon_id>", methods=["GET"])
    def get_pokemon_by_path(pokemon_id):
        pokemon_data = aws.get_pokemon(pokemon_id)
        if pokemon_data:
            return jsonify(pokemon_data), 200
        else:
            return jsonify({"Error": f"Pokemon with ID {pokemon_id} was not found"}), 404
    
    @app.route("/pokemon", methods=["POST"])
    def create_pokemon():
        if not request.is_json:
            return jsonify({"Error": f"Request must be JSON"}), 400
        data = request.get_json()
        is_valid, error_message = validate_pkmn_data(data)
        if not is_valid:
            return jsonify({"Error": error_message}), 400
        
        # Creating some data with defaults
        pokemon_data = {
            "id": data["id"],
            "name": data["name"].strip(),
            "level": data["level"],
            "type": data.get("type", "Normal"),
            "hp": data.get("hp", 50 + (data["level"] * 2)),
            "max_hp": data.get("max_hp", 50 + (data["level"] * 2))
        }
        if aws.create_pokemon(pokemon_data):
            return jsonify(pokemon_data), 201
        else:
            return jsonify({"Error": "The Pokemon already exists"}), 409 # I think it's 409? Will go recheck docs...
        
    @app.route("/pokemon/<int:pokemon_id>", methods=["PUT"])
    def update_pokemon(pokemon_id):
        if not request.is_json:
            return jsonify({"Error": "Request must be JSON"}), 400
        data = request.get_json()

        # Validate w/ validate_pkmn_data
        temp_data = data.copy()
        temp_data["id"] = pokemon_id
        is_valid, error_message = validate_pkmn_data(temp_data)
        if not is_valid:
            return jsonify({"Error": error_message}), 400
        
        # Update Pokemon data
        pokemon_data = {
            "id": pokemon_id,
            "name": data["name"].strip(),
            "level": data["level"],
            "type": data.get("type", "Normal"),
            "hp": data.get("hp", 50 + (data["level"] * 2)),
            "max_hp": data.get("max_hp", 50 + (data["level"] * 2))
        }
        if aws.update_pokemon(pokemon_id, pokemon_data):
            return jsonify(pokemon_data), 200
        else:
            return jsonify({"Error": f"Pokemon with ID {pokemon_id} was not found"}), 404

    @app.route("/pokemon/<int:pokemon_id>", methods=["DELETE"])
    def delete_pokemon(pokemon_id):
        if aws.delete_pokemon(pokemon_id):
            return jsonify({"Note": f"Pokemon with ID {pokemon_id} has been deleted"}), 200
        else:
            return jsonify({"Error": f"Pokemon with ID {pokemon_id} not found"}), 404
    
    # Initialize AWS resources when the app starts
    aws.init_stuff()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)
