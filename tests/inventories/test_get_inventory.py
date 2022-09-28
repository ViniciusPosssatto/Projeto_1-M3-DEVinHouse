from flask import json
import random
from src.app.models.inventory import Inventory

mimetype = 'application/json'
url = "/inventory/"


def test_inventory_get_not_authorized(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    response = client.get(url, headers=headers)
    assert response.status_code == 403
    assert response.json["error"] == "Você não tem permissão"


def test_inventory_get_no_content(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    query_param = "name=12312"
    response = client.get(f"{url}?{query_param}", headers=headers)
    assert response.status_code == 204


def test_inventory_get_success(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    query = Inventory.query.all()
    
    response = client.get(url, headers=headers)

    assert response.status_code == 200
    assert len(response.json) == len(query)
    for item in response.json:
        assert "brand" in item
        assert "description" in item
        assert "id" in item
        assert "product_category_id" in item
        assert "product_code" in item
        assert "template" in item
        assert "title" in item
        assert "user_id" in item
        assert "value" in item
        if item["user_id"]["id"] == None:
            assert item["user_id"]["name"] == "Na empresa"


def test_inventory_get_success_param(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    query_param = {"name": "Headset", "page": 1}
 
    query = Inventory.query.filter(Inventory.title.ilike(f"%{query_param['name']}%")).all()
    response = client.get(f"{url}?name={query_param['name']}&page={query_param['page']}", headers=headers)

    assert response.status_code == 200
    assert len(response.json) == len(query)
    for item in response.json:
        assert "brand" in item
        assert "description" in item
        assert "id" in item
        assert "product_category_id" in item
        assert "product_code" in item
        assert "template" in item
        assert "title" in item
        assert "user_id" in item
        assert "value" in item
        if item["user_id"]["id"] == None:
            assert item["user_id"]["name"] == "Na empresa"


def test_inventory_get_wrong_param_page(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    query_param = {"name": "Headset", "page": -1}
    
    response = client.get(f"{url}?name={query_param['name']}&page={query_param['page']}", headers=headers)

    assert response.status_code == 404


