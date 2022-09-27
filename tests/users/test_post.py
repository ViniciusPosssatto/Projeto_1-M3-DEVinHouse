import random
from flask import json

mimetype = 'application/json'
url = "/user/create"


def test_create_not_authorized(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    
    response = client.post(url, headers=headers)
    assert response.status_code == 403
    assert response.json["error"] == "Você não tem permissão"


def test_create_wrong_id(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    keys = ["city_id", "gender_id", "role_id"]
    keys_wrong_in_request = keys[random.randrange(len(keys))]
    data = {
        "city_id": 1,
        "gender_id": 1,
        "role_id": 1, 
        "name": "Vespucia da Costa",
        "age": "1994-12-15",
        "email": "vespuccia_costa@gmail.com",
        "phone": "12312312",
        "password": "123@456@",
        "cep": "88234800",
        "street": "rua das cove",
        "number_street": "2234",
        "district": "coverones",
        "complement": "atras do muro azul"
    }
    data[keys_wrong_in_request] = -1
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 404
    assert response.json["error"] == "Algum dos IDs não foi encontrado."


def test_create_missing_fields(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    keys = ["city_id", "gender_id", "role_id", "name", "age", "email", "phone", "password", "cep", "street", 
    "number_street", "district"]
    keys_not_have_in_request = keys.pop(random.randrange(len(keys)))
    data = {
        "city_id": 1,
        "gender_id": 1,
        "role_id": 1, 
        "name": "Vespucia da Costa",
        "age": "1994-12-15",
        "email": "vespuccia_costa@gmail.com",
        "phone": "12312312",
        "password": "T123@456@",
        "cep": "88234800",
        "street": "rua das cove",
        "number_street": "2234",
        "district": "coverones",
        "complement": "atras do muro azul"
    }
    del data[keys_not_have_in_request]
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json[keys_not_have_in_request] == [f"O campo {keys_not_have_in_request} é obrigatório."]


def test_create_success(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }

    data = {
        "city_id": 1,
        "gender_id": 1,
        "role_id": 1, 
        "name": "Vespucia da Costa",
        "age": "1994-12-15",
        "email": "vespuccia_costa@gmail.com",
        "phone": "12312312",
        "password": "T123@456@",
        "cep": "88234800",
        "street": "rua das cove",
        "number_street": "2234",
        "district": "coverones",
        "complement": "atras do muro azul"
    }

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json["message"] == "Usuário criado com sucesso."


def test_create_user_failed_exist_user(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    data = {
        "city_id": 1,
        "gender_id": 1,
        "role_id": 1, 
        "name": "Vespucia da Costa",
        "age": "1994-12-15",
        "email": "luislopes@gmail.com",
        "phone": "12312312",
        "password": "T123@456@",
        "cep": "88234800",
        "street": "rua das cove",
        "number_street": "2234",
        "district": "coverones",
        "complement": "atras do muro azul"
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json['error'] == "Erro na criação de Usuário. Email já existe."


def test_create_user_password_failed(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    data = {
        "city_id": 1,
        "gender_id": 1,
        "role_id": 1, 
        "name": "Vespucia da Costa",
        "age": "1994-12-15",
        "email": "vespopes@gmail.com",
        "phone": "12312312",
        "password": "123455667",
        "cep": "88234800",
        "street": "rua das cove",
        "number_street": "2234",
        "district": "coverones",
        "complement": "atras do muro azul"
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["password"] == ['A precisa ter pelo menos 1 caracter especial.']


def test_create_user_phone_failed(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    data = {
        "city_id": 1,
        "gender_id": 1,
        "role_id": 1, 
        "name": "Vespucia da Costa",
        "age": "1994-12-15",
        "email": "vespopes@gmail.com",
        "phone": "(11)12312312",
        "password": "12345@T5667",
        "cep": "88234800",
        "street": "rua das cove",
        "number_street": "2234",
        "district": "coverones",
        "complement": "atras do muro azul"
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["phone"] == ['O telefone não é válido.']
