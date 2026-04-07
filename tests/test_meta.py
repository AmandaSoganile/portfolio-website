def test_meta_returns_version(client):
    response = client.get("/meta")
    assert response.status_code == 200
    data = response.get_json()
    assert "version" in data
    assert "commit_sha" in data
    assert "deployed_at" in data
    assert "environment" in data


def test_meta_version_matches_file(client):
    response = client.get("/meta")
    data = response.get_json()
    assert data["version"] == "0.1.0"
