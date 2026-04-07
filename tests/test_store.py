def test_reactions_start_empty(store):
    assert store.get_reactions(1) == {}


def test_add_reaction_increments(store):
    store.add_reaction(1, "😂")
    store.add_reaction(1, "😂")
    reactions = store.get_reactions(1)
    assert reactions["😂"] == 2


def test_add_reaction_multiple_emojis(store):
    store.add_reaction(1, "😂")
    store.add_reaction(1, "💀")
    reactions = store.get_reactions(1)
    assert reactions["😂"] == 1
    assert reactions["💀"] == 1


def test_reactions_isolated_per_fact(store):
    store.add_reaction(1, "😂")
    store.add_reaction(2, "💀")
    assert store.get_reactions(1) == {"😂": 1}
    assert store.get_reactions(2) == {"💀": 1}


def test_book_submissions_start_empty(store):
    assert store.get_book_submissions() == []


def test_add_book(store):
    store.add_book("Thabo", "Atomic Habits", "James Clear")
    submissions = store.get_book_submissions()
    assert len(submissions) == 1
    assert submissions[0]["name"] == "Thabo"
    assert submissions[0]["title"] == "Atomic Habits"
    assert submissions[0]["author"] == "James Clear"


def test_add_book_without_author(store):
    store.add_book("Thabo", "Atomic Habits")
    submissions = store.get_book_submissions()
    assert submissions[0]["author"] == ""


def test_song_submissions_start_empty(store):
    assert store.get_song_submissions() == []


def test_add_song(store):
    store.add_song("Lerato", "Human Nature", "Michael Jackson", "hits different at 2am")
    submissions = store.get_song_submissions()
    assert len(submissions) == 1
    assert submissions[0]["note"] == "hits different at 2am"


def test_add_song_without_note(store):
    store.add_song("Lerato", "Thriller", "Michael Jackson")
    submissions = store.get_song_submissions()
    assert submissions[0]["note"] == ""
