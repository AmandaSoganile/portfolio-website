def test_books_returns_mine_and_community(client):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.get_json()
    assert "mine" in data
    assert "community" in data


def test_books_mine_has_seven_entries(client):
    response = client.get("/books")
    data = response.get_json()
    assert len(data["mine"]) == 7


def test_books_mine_has_required_fields(client):
    response = client.get("/books")
    data = response.get_json()
    for book in data["mine"]:
        assert "title" in book
        assert "author" in book


def test_books_community_starts_empty(client):
    response = client.get("/books")
    data = response.get_json()
    assert data["community"] == []


def test_post_book_valid(client):
    response = client.post("/books", json={"name": "Thabo", "title": "The Subtle Art"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_post_book_appears_in_community(client):
    client.post("/books", json={"name": "Thabo", "title": "The Subtle Art"})
    response = client.get("/books")
    data = response.get_json()
    assert len(data["community"]) == 1
    assert data["community"][0]["name"] == "Thabo"
    assert data["community"][0]["title"] == "The Subtle Art"


def test_post_book_missing_name_rejected(client):
    response = client.post("/books", json={"title": "Atomic Habits"})
    assert response.status_code == 400


def test_post_book_missing_title_rejected(client):
    response = client.post("/books", json={"name": "Thabo"})
    assert response.status_code == 400
