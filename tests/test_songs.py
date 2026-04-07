def test_songs_returns_mine_and_community(client):
    response = client.get("/songs")
    assert response.status_code == 200
    data = response.get_json()
    assert "mine" in data
    assert "community" in data


def test_songs_mine_has_five_entries(client):
    response = client.get("/songs")
    data = response.get_json()
    assert len(data["mine"]) == 5


def test_songs_mine_has_required_fields(client):
    response = client.get("/songs")
    data = response.get_json()
    for song in data["mine"]:
        assert "title" in song
        assert "artist" in song


def test_songs_community_starts_empty(client):
    response = client.get("/songs")
    data = response.get_json()
    assert data["community"] == []


def test_post_song_valid(client):
    response = client.post("/songs", json={
        "name": "Lerato",
        "title": "Human Nature",
        "artist": "Michael Jackson",
        "note": "hits different at 2am"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_post_song_appears_in_community(client):
    client.post("/songs", json={
        "name": "Lerato",
        "title": "Human Nature",
        "artist": "Michael Jackson",
        "note": "hits different at 2am"
    })
    response = client.get("/songs")
    data = response.get_json()
    assert len(data["community"]) == 1
    assert data["community"][0]["note"] == "hits different at 2am"


def test_post_song_missing_name_rejected(client):
    response = client.post("/songs", json={"title": "Billie Jean", "artist": "Michael Jackson"})
    assert response.status_code == 400


def test_post_song_missing_title_rejected(client):
    response = client.post("/songs", json={"name": "Lerato", "artist": "Michael Jackson"})
    assert response.status_code == 400


def test_post_song_note_is_optional(client):
    response = client.post("/songs", json={"name": "Lerato", "title": "Thriller"})
    assert response.status_code == 200
