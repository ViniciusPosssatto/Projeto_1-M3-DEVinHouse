from flask import json
import random
from src.app.models.inventory import Inventory

mimetype = 'application/json'
url = "/inventory/"


def test_inventory_patch_not_authorized(client):
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
    id = 5
    response = client.patch(f"{url}{id}", data=json.dumps(data), headers=headers)
    assert response.status_code == 403
    assert response.json["error"] == "Você não tem permissão"


def test_inventory_patch_not_found(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
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
    id = -5
    response = client.patch(f"{url}{id}", data=json.dumps(data), headers=headers)
    assert response.status_code == 404


def test_inventory_patch_not_update_fields_id(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    keys = ["id", "product_category_id", "product_code"]
    keys_wrong_in_request = keys[random.randrange(len(keys))]
    data = {
        "user_id": 3,
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    data[keys_wrong_in_request] = 1
    id = 5
    response = client.patch(f"{url}{id}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json[keys_wrong_in_request] == ['Unknown field.']


def test_inventory_patch_not_update_value_to_zero(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    data = {
        "user_id": 3,
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    data["value"] = 0
    id = 5
    response = client.patch(f"{url}{id}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["value"] == ['O valor não pode ser menor ou igual a 0.']


def test_inventory_patch_missing_fields(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    keys = ["title", "brand", "template", "description"]
    keys_not_have_in_request = keys.pop(random.randrange(len(keys)))
    data = {
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    data[keys_not_have_in_request] = 1
    id = 5
    response = client.patch(f"{url}{id}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json[keys_not_have_in_request] == ['Not a valid string.']


def test_inventory_value_failed(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }

    data = {
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    data["value"] = -1
    id = 5
    response = client.patch(f"{url}{id}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json["value"] == ['O valor não pode ser menor ou igual a 0.']


def test_inventory_patch_field_excedeeded_limit(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        "Authorization": f"Bearer {logged_in_client}"
    }
    keys = ["title", "brand", "template", "description"]
    keys_wrong_in_request = keys[random.randrange(len(keys))]
    data = {
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    data[keys_wrong_in_request] = "Lorem Ipsum has been the industry's standard dummy t Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. "
    id = 1
    response = client.patch(f"{url}{id}", data=json.dumps(data), headers=headers)
    assert response.status_code == 404
    assert response.json["error"] == 'Item não encontrado.'

def test_inventory_change_fields_not_null(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    keys = ["title", "brand", "template", "description", "value"]
    keys_wrong_in_request = keys[random.randrange(len(keys))]
    data = {
        "title" : "Camera HD",
        "value" : 1350,
        "brand" : "Tekpix",
        "template" : "123-tek",
        "description" : "Camera full hd, grava audio e video" 
    }
    data[keys_wrong_in_request] = None 
    id = 5
    response = client.patch(f"{url}{id}", data=json.dumps(data), headers=headers)
    assert response.status_code == 400
    assert response.json[keys_wrong_in_request] == ['Field may not be null.']
