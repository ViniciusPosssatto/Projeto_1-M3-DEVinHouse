from typing import List
from flask import json
import random


mimetype = 'application/json'
url = "/user/"


def test_get_not_authorized(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    query_param = "name=arthur"
   
    response = client.get(f"{url}?{query_param}", headers=headers)
    assert response.status_code == 403
    assert response.json["error"] == "Você não tem permissão"


def test_get_wrong_query_param(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    query_param = "name=12312"
    response = client.get(f"{url}?{query_param}", headers=headers)
    assert response.status_code == 204


def test_get_all_success(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
   
    response = client.get(f"{url}", headers=headers)
    assert response.status_code == 200
    assert "id" in response.json[0]
    assert "name" in response.json[0]
    assert "email" in response.json[0]
    assert "phone" in response.json[0]
    assert "role.name" in response.json[0]


def test_get_success_one_query_param(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    keys = {"name": "name=Luis", "page": "page=1"}
    query_param = random.choice(list(keys.values()))

    response = client.get(f"{url}?{query_param}", headers=headers)
    assert response.status_code == 200

        
def test_get_success_fields(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    query_param = "name=Luis"
    response = client.get(f"{url}?{query_param}", headers=headers)
    assert response.status_code == 200
    assert "id" in response.json[0]
    assert "name" in response.json[0]
    assert "email" in response.json[0]
    assert "phone" in response.json[0]
    assert "role.name" in response.json[0]


def test_get_success_query_param_name_page(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    query_param = "name=Luis&page=1"
   
    response = client.get(f"{url}?{query_param}", headers=headers)
    assert response.status_code == 200


def test_get_failed_page_param(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    query_param = "page=-1"
   
    response = client.get(f"{url}?{query_param}", headers=headers)
    assert response.status_code == 404
