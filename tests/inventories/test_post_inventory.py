from flask import json
import random
from src.app.models.inventory import Inventory

mimetype = 'application/json'
url = "/inventory/create"


def test_inventory_post_not_authorized(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "product_category_id" : 3,
        "user_id" : 4,
        "product_code" : 123123,
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 403
    assert response.json["error"] == "Você não tem permissão"


def test_inventory_wrong_product_code(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    data = {
        "product_category_id" : 3,
        "user_id" : 4,
        "product_code" : "asd123123",
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["product_code"] == ["Não é um campo válido."]


def test_inventory_product_code_exists(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    query = Inventory.query.all()
    data = {
        "product_category_id" : 3,
        "user_id" : 4,
        "product_code" : f"{query[0].product_code}",
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["error"] == "Esse código de produto já existe"


def test_inventory_product_code_failed(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }

    data = {
        "product_category_id" : 3,
        "user_id" : 4,
        "product_code" : 1234567890,
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["product_code"] == ['O código do produto deve ser maior que 0 com no máximo 8 dígitos.']


def test_inventory_field_excedeeded_limit(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    keys = ["title", "brand", "template", "description"]
    keys_wrong_in_request = keys[random.randrange(len(keys))]
    data = {
        "product_category_id" : 3,
        "user_id" : 4,
        "product_code" : 123456,
        "title" : "Alguma coisa",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    data[keys_wrong_in_request] = "Lorem Ipsum has been the industry's standard dummy t Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. "
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["error"] == "Erro ao cadastrar item"


def test_inventory_wrong_id(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    keys = ["product_category_id", "user_id"]
    keys_wrong_in_request = keys[random.randrange(len(keys))]
    data = {
        "product_category_id" : 3,
        "user_id" : 4,
        "product_code" : 1232341,
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    data[keys_wrong_in_request] = -1
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["error"] == "Erro ao cadastrar item"


def test_inventory_value_failed(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }

    data = {
        "product_category_id" : 3,
        "user_id" : 4,
        "product_code" : 1232341,
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    data["value"] = -1
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["value"] == ['O valor não pode ser menor ou igual a 0.']


def test_inventory_missing_fields(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    keys = ["product_category_id", "product_code", "title", "brand", "template", "description"]
    keys_wrong_not_have_in_request = keys.pop(random.randrange(len(keys)))
    data = {
        "product_category_id" : 3,
        "user_id" : 4,
        "product_code" : 1232341,
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    del data[keys_wrong_not_have_in_request]
    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json[keys_wrong_not_have_in_request] == [f'O campo {keys_wrong_not_have_in_request} é obrigatório.']


def test_inventory_success_not_have_user_id(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }

    data = {
        "product_category_id" : 3,
        "product_code" : 1232341,
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json["message"] == 'Item cadastrado com sucesso'


def test_inventory_create_success(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }

    data = {
        "product_category_id" : 3,
        "user_id" : 5,
        "product_code" : 1232341,
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 201
    assert response.json["message"] == 'Item cadastrado com sucesso'
