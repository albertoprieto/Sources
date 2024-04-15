import requests
import json

lambda_url = "https://d60074mm23.execute-api.us-west-2.amazonaws.com/test/"

# Datos que deseas enviar en el cuerpo de la solicitud POST

data = {
    "id": "1",
    "name": "xxx",
    "price": 5
}

json_data = json.dumps(data)
headers = {
    "Content-Type": "application/json"
}


#response = requests.post(lambda_url, data=json_data, headers=headers)
#print(response.text)
#response = requests.get(lambda_url)
#print(response.status_code)
#print(response.text)



# Datos para la solicitud DELETE

delete_data = {
    'id': '1'
}



# Datos para la solicitud PATCH


patch_data = {
    'id': '1',
    'fieldName': 'name',
    'updateValue': 'jose alberto'
}

# Realizar solicitud DELETE
delete_response = requests.delete(lambda_url, json=delete_data)
print('Respuesta DELETE:', delete_response.json())

# Realizar solicitud PATCH
#patch_response = requests.patch(lambda_url, json=patch_data)
#print('Respuesta PATCH:', patch_response.json())

#response = requests.get(lambda_url)
#print(response.status_code)
#print(response.text)
