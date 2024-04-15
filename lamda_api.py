import json
import boto3

#Cambiar el nombre de la tabla.
#Cambiar los valores del post ya que son los que reconocerá.

dynamodb_client = boto3.client('dynamodb')
table_name = 'http-crud-tutorial-items'
dynamodbTableName = "http-crud-tutorial-items"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(dynamodbTableName)

def lambda_handler(event, context):
    body = None
    status_code = 200
    headers = {'Content-Type': 'application/json'}

    try:

        http_method = event['httpMethod']
        
        if http_method == 'POST':
            request_body = json.loads(event['body'])
            dynamodb_client.put_item(
                TableName=table_name,
                Item={
                    'id': {'S': request_body.get('id')},
                    'price': {'N': str(request_body.get('price'))},
                    'name': {'S': request_body.get('name')}
                }
            )
            body = f"Item {request_body.get('id')} created successfully"
        
        elif http_method == 'GET':

            response = dynamodb_client.scan(TableName=table_name)
            items = response.get('Items', [])
            body = items
        

        elif http_method =='PATCH':
            hold = json.loads(event['body'])


            response = table.update_item(
                Key={'id': hold['id']},
                UpdateExpression=f"SET #{hold['fieldName']} = :value",
                ExpressionAttributeNames={f"#{hold['fieldName']}": hold['fieldName']},
                ExpressionAttributeValues={':value': hold['updateValue']},
                ReturnValues='UPDATED_NEW'
            )

            body = {
                'Operation': 'UPDATE',
                'Message': 'SUCCESS',
                'UpdatedAttributes': response
            }

        elif http_method == 'DELETE':
            hold = json.loads(event['body'])
            hold_id = hold.get('id')
            response = table.delete_item(
                Key={
                    "id": hold_id
                },
                ReturnValues="ALL_OLD"
            )
            body = {
                "Operation": "DELETE",
                "Message": "SUCCESS",
                "deltedItem": response
            }

        else:
            raise ValueError("Unsupported HTTP method")
    
    except Exception as e:
        status_code = 400
        body = {'error': str(e)}

    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': headers
    }
