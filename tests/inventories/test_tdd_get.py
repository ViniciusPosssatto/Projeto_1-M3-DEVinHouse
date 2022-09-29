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
    id = 3
    response = client.get(f"{url}{id}", headers=headers)
    assert response.status_code == 403
    assert response.json["error"] == "Você não tem permissão"


def test_inventory_missing_param(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }

    response = client.get(url, headers=headers)
    assert response.status_code == 400


def test_inventory_wrong_param(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    id = "erro"
    response = client.get(f"{url}{id}", headers=headers)
    assert response.status_code == 400


def test_inventory_get_not_exists(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    id = -1
    response = client.get(f"{url}{id}", headers=headers)
    assert response.status_code == 404


def test_inventory_get_success(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    id = 1
    response = client.get(f"{url}{id}", headers=headers)
    assert response.status_code == 200
    assert response.json == "pass"# retornar todos os dados do item 
