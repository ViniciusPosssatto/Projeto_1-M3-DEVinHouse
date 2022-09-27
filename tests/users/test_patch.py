from flask import json
import random


mimetype = 'application/json'
url = "/user"


def test_update_not_authorized(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    param = 3
    data = {
        "name": "Marcos de Freitas",
        "age": "1990-11-3",
        "email": "testeeee@testing.com",
        "phone": "12312312",
        "password": "123@456@"
    }
    response = client.patch(f"{url}/{param}", data=json.dumps(data), headers=headers)
    assert response.status_code == 403
    assert response.json["error"] == "Você não tem permissão"


def test_update_not_found(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    query_param = -3
    data = {
        "name": "Marcos de Freitas",
        "age": "1990-11-3",
        "email": "testeeee@testing.com",
        "phone": "12312312",
        "password": "123@456@"
    }
    response = client.patch(f"{url}/{query_param}", data=json.dumps(data), headers=headers)
    assert response.status_code == 404


def test_update_not_authorized_update_id(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    param = 4
    data = {
        "id": 34234,
        "name": "Marcos de Freitas",
        "age": "1990-11-3",
        "email": "marcos_freitas@gmail.com",
        "phone": "12312312",
        "password": "123@456@"
    }
    
    response = client.patch(f"{url}/{param}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["id"] == ['Unknown field.']


def test_update_missing_fields(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    keys = ["name", "email", "password"]
    keys_not_have_in_request = keys.pop(random.randrange(len(keys)))
    param = 4
    data = {
        "name": "Marcos de Freitas",
        "age": "1990-11-3",
        "email": "marcos_freitas@gmail.com",
        "phone": "12312312",
        "password": "123@456@"
    }
    del data[keys_not_have_in_request]
    response = client.patch(f"{url}/{param}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json[keys_not_have_in_request] == [f"O campo {keys_not_have_in_request} é obrigatório."]


def test_update_age_not_valid(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    param = 4
    data = {
        "name": "Marcos de Freitas",
        "age": "111111",
        "email": "marcos_freitas@gmail.com",
        "phone": "12312312",
        "password": "123@456@"
    }
    
    response = client.patch(f"{url}/{param}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["age"] == ["Not a valid date."]


def test_update_email_not_valid(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    param = 5
    data = {
        "name": "Marcos de Freitas",
        "age": "1990-11-3",
        "email": "marcosgmail.com",
        "phone": "12312312",
        "password": "123@Teeeste"
    }
    
    response = client.patch(f"{url}/{param}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["email"] == ["Não é um campo válido."]


def test_update_senha_not_valid(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    param = 5
    data = {
        "name": "Marcos de Freitas",
        "age": "1990-11-3",
        "email": "marcos_freitas@gmail.com",
        "phone": "12312312",
        "password": "123"
    }
    
    response = client.patch(f"{url}/{param}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json == {"password": ["A senha precisa ser maior ou igual a 8."]}


def test_update_missing_all_fields(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    param = 5
    data = {}
    
    response = client.patch(f"{url}/{param}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json == {"email": ["O campo email é obrigatório."],"name": ["O campo name é obrigatório."],"password": ["O campo password é obrigatório."]}


def test_update_exists_email(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    param = 5
    data = {
        "name": "Luis de Freitas",
        "age": "1990-11-3",
        "email": "luislopes@gmail.com",
        "phone": "12312312",
        "password": "123@Teste"
    }
    
    response = client.patch(f"{url}/{param}", data=json.dumps(data), headers=headers)
    assert response.status_code == 409
    assert response.json == {'error': 'Email já existe.'}


