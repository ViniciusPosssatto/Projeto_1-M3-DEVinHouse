from flask import json
import random
from src.app.models.user import User


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
    for item in response.json:
        assert "id" in item
        assert "name" in item
        assert "email" in item
        assert "phone" in item
        assert "role.name" in item


def test_get_count_all_success(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    all_users = User.query.all()
    response = client.get(f"{url}", headers=headers)
    assert response.status_code == 200
    assert len(all_users) == len(response.json)


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
    for item in response.json:
        assert "id" in item
        assert "name" in item
        assert "email" in item
        assert "phone" in item
        assert "role.name" in item


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
    all_users = User.query.all()
    per_page = 20
    pages = round(len(all_users) / per_page)
    page_wrong = pages + 1
    query_param = f"page={page_wrong}"
   
    response = client.get(f"{url}?{query_param}", headers=headers)
    assert response.status_code == 404
