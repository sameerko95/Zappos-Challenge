import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    db = boto3.resource('dynamodb')
    table = db.Table('restaurants')
    cache = boto3.client('elasticache')

    restaurant_ids = event['params']['querystring']['ids'].split(",")
    print(type(restaurant_ids))
    print(restaurant_ids)
    for i in restaurant_ids:
        response = table.scan(
            Select = 'ALL_ATTRIBUTES',
            FilterExpression = Attr('id').equals(i)
        )
        print(response)
        response = table.delete_item(
            Key={
                'id': response['Items'][0]['id']
            }
        )
        cache_response = cache.remove_tags_from_resource(
            ResourceName = "arn:aws:elasticache:us-east-2:794695955072:cluster:restaurants-data",
            TagKeys = [
                i,
            ]
        )
        print(cache_response)
    return "Deletion Complete"