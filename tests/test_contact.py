def test_contact_valid_submission(client):
    response = client.post("/contact", json={
        "name": "Thabo",
        "slack_email": "thabo@company.slack.com",
        "message": "Love your work!"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_contact_missing_name_rejected(client):
    response = client.post("/contact", json={
        "slack_email": "thabo@company.slack.com",
        "message": "Hello"
    })
    assert response.status_code == 400


def test_contact_missing_email_rejected(client):
    response = client.post("/contact", json={
        "name": "Thabo",
        "message": "Hello"
    })
    assert response.status_code == 400


def test_contact_missing_message_rejected(client):
    response = client.post("/contact", json={
        "name": "Thabo",
        "slack_email": "thabo@company.slack.com"
    })
    assert response.status_code == 400


def test_contact_empty_fields_rejected(client):
    response = client.post("/contact", json={
        "name": "",
        "slack_email": "",
        "message": ""
    })
    assert response.status_code == 400
