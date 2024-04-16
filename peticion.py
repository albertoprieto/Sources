import requests
import json
import decimal
lambda_url = "https://vm24942awk.execute-api.us-west-2.amazonaws.com/mavi_test/"

# Datos que deseas enviar en el cuerpo de la solicitud POST

data = {
    "id": "2",
    "name": "hola",
    "price": 2
}

data = {
    'id':'1'
}

json_data = json.dumps(data)

headers = {
    "Content-Type": "application/json"
}

#response = requests.get(lambda_url)
response = requests.get(lambda_url, data=json_data, headers=headers)
#response = requests.post(lambda_url, data=json_data, headers=headers)
#response = requests.put(lambda_url, data=json_data, headers=headers)

print(response.text)

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
#delete_response = requests.delete(lambda_url, json=delete_data)
#print('Respuesta DELETE:', delete_response.json())

# Realizar solicitud PATCH
#patch_response = requests.patch(lambda_url, json=patch_data)
#print('Respuesta PATCH:', patch_response.json())

#response = requests.get(lambda_url)
#print(response.status_code)
#print(response.text)
