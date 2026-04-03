ALLOWED_EMOJIS = {"😂", "💀", "😭", "🫶", "👀"}


def test_fun_facts_all_returns_list(client):
    response = client.get("/fun-fact/all")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 10


def test_fun_facts_have_required_fields(client):
    response = client.get("/fun-fact/all")
    data = response.get_json()
    for fact in data:
        assert "id" in fact
        assert "fact" in fact
        assert "reactions" in fact
        assert isinstance(fact["reactions"], dict)


def test_reactions_start_empty(client):
    response = client.get("/fun-fact/all")
    data = response.get_json()
    assert data[0]["reactions"] == {}


def test_get_reactions_for_fact(client):
    response = client.get("/fun-fact/1/reactions")
    assert response.status_code == 200
    data = response.get_json()
    assert "fact_id" in data
    assert "reactions" in data
    assert data["fact_id"] == 1


def test_post_valid_reaction(client):
    response = client.post("/fun-fact/1/react", json={"emoji": "😂"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["reactions"]["😂"] == 1


def test_post_reaction_increments(client):
    client.post("/fun-fact/1/react", json={"emoji": "😂"})
    client.post("/fun-fact/1/react", json={"emoji": "😂"})
    response = client.post("/fun-fact/1/react", json={"emoji": "😂"})
    data = response.get_json()
    assert data["reactions"]["😂"] == 3


def test_post_invalid_emoji_rejected(client):
    response = client.post("/fun-fact/1/react", json={"emoji": "🍕"})
    assert response.status_code == 400


def test_post_missing_emoji_rejected(client):
    response = client.post("/fun-fact/1/react", json={})
    assert response.status_code == 400


def test_invalid_fact_id_returns_404(client):
    response = client.get("/fun-fact/999/reactions")
    assert response.status_code == 404
