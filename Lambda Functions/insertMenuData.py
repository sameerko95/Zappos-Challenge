import boto3
import hashlib

def lambda_handler(event, context):
    name = event['params']['querystring']['name']
    restaurant_id = event['params']['querystring']['restaurant_id']
    price = event['params']['querystring']['price']
    
    pkey = name + restaurant_id + price
    pkey_hash = hashlib.sha256(pkey.encode('utf-8'))
    db = boto3.resource('dynamodb')
    table = db.Table('menu_items')

    insert = table.put_item(
        Item = {
            'id': pkey_hash.hexdigest(),
            'name': name,
            'restaurant_id': restaurant_id,
            'price': price,
        }
    )

    return "success"