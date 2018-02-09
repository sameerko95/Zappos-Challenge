import boto3
import hashlib

def lambda_handler(event, context):
    name = event['params']['querystring']['name']
    location = event['params']['querystring']['location']
    zip_code = event['params']['querystring']['zip']
    
    pkey = name + location + zip_code
    pkey_hash = hashlib.sha256(pkey.encode('utf-8'))
    db = boto3.resource('dynamodb')
    table = db.Table('restaurants')

    insert = table.put_item(
        Item = {
            'id': pkey_hash.hexdigest(),
            'name': name,
            'location': location,
            'zip': zip_code,
            'timestamp': int(time.time())
        }
    )

    return "success"