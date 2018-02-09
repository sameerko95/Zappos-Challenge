import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    table_name = event['params']['querystring']['table_name']
    param_name = event['params']['querystring']['param_name']
    param_value = event['params']['querystring']['param_value']
    
    cache = boto3.client('elasticache')
    tags_list = cache.list_tags_for_resource(ResourceName="arn:aws:elasticache:us-east-2:794695955072:cluster:restaurants-data")
    search_result = []
    if len(tags_list['TagList'])>0:
        for element in tags_list["TagList"]:
            if param_value in element['Value']:
                values = element['Value'].split(":")
                element_dict = {
                    'id' : values[0],
                    'name' : values[1],
                    'location' : values[2],
                    'zip' : values[3]
                }
                search_result.append(element_dict)
        return search_result

    else:
        db = boto3.resource('dynamodb')
        table = db.Table(table_name)
        
        search_result = table.scan(
            Select = 'ALL_ATTRIBUTES',
            FilterExpression = Attr(param_name).equals(param_value)
        )
        for item in search_result['Items']:
            identity = item['id']
            name = item['name']
            location = item['location']
            zip_code = item['zip']
            values = identity + ":" + name + ":" + location + ":" + zip_code
            response = cache.add_tags_to_resource(
                ResourceName = "arn:aws:elasticache:us-east-2:794695955072:cluster:restaurants-data",
                Tags = [
                    {
                        'Key' : identity,
                        'Value' : values
                    }
                ]
            )

        return search_result['Items']