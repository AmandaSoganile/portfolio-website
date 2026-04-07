def test_about_returns_name(client):
    response = client.get("/about")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Amanda Fezile Soganile"


def test_about_has_required_fields(client):
    response = client.get("/about")
    data = response.get_json()
    for field in ["bio", "tagline", "currently_learning", "mission", "things_i_love"]:
        assert field in data, f"Missing field: {field}"


def test_projects_returns_list(client):
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_projects_farmcare_exists(client):
    response = client.get("/projects")
    data = response.get_json()
    ids = [p["id"] for p in data]
    assert "farmcare" in ids
