import json

def lambda_handler(event, context):
    # Obtener el método HTTP y el cuerpo de la solicitud
    http_method = event['httpMethod']
    request_body = json.loads(event['body'])

    # Verificar si la solicitud es PUT
    if http_method == 'PUT':
        # Acceder a los datos de la solicitud PUT
        item_id = request_body.get('id')
        new_price = request_body.get('price')
        new_name = request_body.get('name')

        # Realizar la operación PUT (actualización) en DynamoDB
        dynamodb_client.update_item(
            TableName=table_name,
            Key={'id': {'S': item_id}},
            UpdateExpression='SET price = :price, name = :name',
            ExpressionAttributeValues={
                ':price': {'N': str(new_price)},
                ':name': {'S': new_name}
            }
        )
        # Crear una respuesta
        body = f"Item {item_id} updated successfully"

        response = {
            "statusCode": 200,
            "body": body
        }
        return response
    else:
        # Manejar otros métodos HTTP (GET, POST, DELETE, etc.) según sea necesario
        # Si no es una solicitud PUT, puede devolver un error o una respuesta adecuada
        response = {
            "statusCode": 400,
            "body": "Unsupported HTTP method"
        }
        return response
