'''Adding this file in part 3 for all the new aws stuff like initiating the DynamoDB and S3 bucket things. I'll also put in some CRUD command stuff (create_pokemon, get_pokemon, get_all_pokemon, update_pokemon, and delete_pokemon) all in the DB and S3 so that they work the same. I later changed this into a class so that I could call on stuff easier in api.py'''

# Imports
import boto3
import json
import os
from botocore.exceptions import ClientError

class PokemonAWS:
    def __init__(self):
        ENDPOINT_URL = os.getenv("ENDPOINT_URL", "http://localhost:4566") # localstack
        self.dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=ENDPOINT_URL,
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test"
        )
        self.s3 = boto3.client(
            "s3",
            endpoint_url=ENDPOINT_URL,
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test"
        )
        self.bucket_name = "pokemon-bucket"
        self.table_name = "pokemon-table"
        self.table = self.dynamodb.Table(self.table_name)

    def init_stuff(self):
        # DynamoDB
        try:
            self.dynamodb.create_table(
                TableName="pokemon-table",
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
                BillingMode="PAY_PER_REQUEST"
            )
            print("Created the DynamoDB table (pokemon-table)")
            self.table.wait_until_exists()
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("The table already exists")
            else:
                print(f"Error: {e}")
        
        # S3
        try:
            self.s3.create_bucket(Bucket=self.bucket_name)
            print(f"Created the S3 bucket ({self.bucket_name})")
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print("The bucket already exists")
            else:
                print(f"Error: {e}")

    # CRUD operations for both db and bucket
    def create_pokemon(self, pokemon_data):
        try:
            self.table.put_item( # going in table
                Item=pokemon_data,
                ConditionExpression='attribute_not_exists(id)'
            )
            self.s3.put_object( # going in bucket
                Bucket=self.bucket_name,
                Key=f"pokemon/{pokemon_data['id']}.json",
                Body=json.dumps(pokemon_data),
                ContentType='application/json'
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return False # for if the pokemon already exists
            print(f"Error: {e}")
            return False

    def get_pokemon(self, pokemon_id):
        try:
            response = self.table.get_item(Key={'id': pokemon_id})
            item = response.get('Item')
            if item:
                # Make numeric fields are integers - this caused me about 4281 problems :/
                item["id"] = int(item["id"])
                item["level"] = int(item["level"])
                item["hp"] = int(item["hp"])
                item["max_hp"] = int(item["max_hp"])
            return item
        except ClientError as e:
            print(f"Error: {e}")
            return None
    
    def get_all_pokemon(self):
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error: {e}")
            return []

    def update_pokemon(self, pokemon_id, pokemon_data):
        try:
            if not self.get_pokemon(pokemon_id): # check that exists
                return False
            pokemon_data["id"] = pokemon_id # make sure ids match
            self.table.put_item(Item=pokemon_data)
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=f"pokemon/{pokemon_id}.json",
                Body=json.dumps(pokemon_data),
                ContentType='application/json'
            )
            return True
        except ClientError as e:
            print(f"Error: {e}")
            return False
    
    def delete_pokemon(self, pokemon_id):
        try:
            if not self.get_pokemon(pokemon_id):
                return False
            self.table.delete_item(Key={'id': pokemon_id})
            self.s3.delete_object(Bucket=self.bucket_name, Key=f"pokemon/{pokemon_id}.json")
            return True
        except ClientError as e:
            print(f"Error: {e}")
            return False
