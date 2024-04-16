import json
import boto3

#Cambiar el nombre de la tabla.
#Cambiar los valores del post ya que son los que reconocerá.

dynamodb_client = boto3.client('dynamodb')
table_name = 'mavi_crud_jap'
dynamodbTableName = "mavi_crud_jap"
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
        

        # Lógica para manejar solicitudes GET
        elif http_method == 'GET':
            # Obtener los parámetros de la consulta de la solicitud GET
            query_params = json.loads(event['body'])
            if query_params:
                # Verificar si se proporcionó un parámetro 'id' en la solicitud GET
                id_to_find = query_params.get('id')
                if id_to_find:
                    # Si se proporciona 'id', buscar el elemento correspondiente en la tabla
                    response = dynamodb_client.get_item(
                        TableName=table_name,
                        Key={'id': {'S': id_to_find}}
                    )
                    item = response.get('Item')
                    if item:
                        # Si se encontró el elemento, devolverlo
                        body = item
                    else:
                        # Si no se encontró el elemento, devolver un mensaje de error
                        body = {'error': 'Item not found'}
                else:
                    # Si no se proporciona 'id', devolver un mensaje de error
                    body = {'error': 'ID parameter is missing'}
            else:
                # Si no se proporcionan parámetros de consulta, devolver todos los elementos de la tabla
                response = dynamodb_client.scan(TableName=table_name)
                items = response.get('Items', [])
                body = items

        elif http_method == 'PUT':
            request_body = json.loads(event['body'])
            response = table.update_item(
                Key={'id': request_body.get('id')},
                UpdateExpression='SET price = :price, #n = :name',
                ExpressionAttributeNames={'#n': 'name'},
                ExpressionAttributeValues={
                    ':price': request_body.get('price'),
                    ':name': request_body.get('name')
                },
                ReturnValues='UPDATED_NEW'
            )
            body = {
                'Operation': 'UPDATE',
                'Message': 'SUCCESS',
                'UpdatedAttributes': response['Attributes']
            }



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
        'body': json.dumps(body, default=decimal_default),
        'headers': headers
    }


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
