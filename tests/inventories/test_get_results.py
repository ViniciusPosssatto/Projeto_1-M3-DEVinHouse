from flask import json
import random


mimetype = 'application/json'
url = "/inventory/results"


def test_get_not_authorized(client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    response = client.get(url, headers=headers)
    assert response.status_code == 403
    assert response.json["error"] == "Você não tem permissão"


def test_get_success(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
   
    response = client.get(f"{url}", headers=headers)
    assert response.status_code == 200
    assert "total_items" in response.json
    assert "total_items_loaned" in response.json
    assert "total_items_price" in response.json
    assert "total_users" in response.json


def test_get_param_failed(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    param = 3
    response = client.get(f"{url}/{param}", headers=headers)
    assert response.status_code == 404


# def test_get_missing_key(client, logged_in_client):
#     headers = {
#         'Content-Type': mimetype,
#         'Accept': mimetype,
#         'Authorization': f'Bearer {logged_in_client}'
#     }
#     keys = ["total_items", "total_items_loaned", "total_items_price", "total_users"]
#     key_not_have_in_response = keys.pop(random.randrange(len(keys)))
#     response = client.get(url, headers=headers)
#     print(key_not_have_in_response)
#     resp = response.json
#     resp.pop(key_not_have_in_response)
#     print(resp)
#     assert response.status_code == 200
#     assert response.json[key_not_have_in_response] == "asdas"
