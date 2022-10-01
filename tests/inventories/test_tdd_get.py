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


def test_inventory_wrong_param(client, logged_in_client):
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': f'Bearer {logged_in_client}'
    }
    id = "erro"
    response = client.get(f"{url}{id}", headers=headers)
    assert response.status_code == 404


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
    assert "id" in response.json
    assert "product_category_id" in response.json
    assert "user" in response.json
    assert "title" in response.json
    assert "product_code" in response.json
    assert "value" in response.json
    assert "brand" in response.json
    assert "template" in response.json
    assert "description" in response.json
    if response.json['user'] != "Na empresa":
        assert "id" in response.json["user"]
        assert "name" in response.json["user"]
        assert "email" in response.json["user"]
        assert "phone" in response.json["user"]
        assert "role.name" in response.json["user"]
    else:
        assert response.json["user"] == "Na empresa"
