import random
from flask import json

mimetype = 'application/json'
url = "/user/role"


def test_create_role_not_authorized(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    
    response = client.post(url, headers=headers)
    assert response.status_code == 403
    assert response.json["error"] == "Você não tem permissão"


def test_create_missing_fields(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    keys = ["description", "name", "permissions"]
    keys_not_have_in_request = keys.pop(random.randrange(len(keys)))
    data = {
        "description": "Algum cargo",
        "name": "Admin",
        "permissions": [2, 4]
    }
    del data[keys_not_have_in_request]
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json[keys_not_have_in_request] == [f"O campo {keys_not_have_in_request} é obrigatório."]


def test_create_wrong_id_permissions(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    data = {
        "description": "Algum cargo",
        "name": "Admin",
        "permissions": [-1]
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["error"] == "As permissões enviadas são inválidas"


def test_create_role_success(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    data = {
        "description": "Algum cargo",
        "name": "Admin",
        "permissions": [3, 4]
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json["message"] == "O cargo foi criado com sucesso"


def test_create_role_exists(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    data = {
        "description": "Alguma coisa ai",
        "name": "Admin",
        "permissions": [1, 2, 3, 4]
    }
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["error"] == "Este cargo já existe"


def test_create_role_excedeeded_limit_field(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    keys = ["description", "name"]
    keys_wrong_in_request = keys[random.randrange(len(keys))]
    txt = "Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text."
    data = {
        "description": "Alguma coisa ai",
        "name": "Admin",
        "permissions": [1, 2, 3, 4]
    }
    data[keys_wrong_in_request] = txt
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["error"] == "Algo inesperado aconteceu"
