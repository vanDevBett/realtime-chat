def test_get_room_messages_empty(client, registered_user):
    response = client.get("/chat/rooms/general/messages")
    assert response.status_code == 200
    assert response.json() == []


def test_get_room_messages_after_save(client, db, registered_user):
    from app.services.chat_service import save_message
    from app.models.user import User

    user = db.query(User).filter(User.email == "user@test.com").first()
    save_message(db, content="Hello world", room="general", user_id=user.id)

    response = client.get("/chat/rooms/general/messages")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["content"] == "Hello world"
    assert response.json()[0]["full_name"] == "Test User"


def test_get_different_rooms(client, db, registered_user):
    from app.services.chat_service import save_message
    from app.models.user import User

    user = db.query(User).filter(User.email == "user@test.com").first()
    save_message(db, content="General message", room="general", user_id=user.id)
    save_message(db, content="Random message", room="random", user_id=user.id)

    general = client.get("/chat/rooms/general/messages")
    random = client.get("/chat/rooms/random/messages")

    assert len(general.json()) == 1
    assert len(random.json()) == 1
    assert general.json()[0]["content"] == "General message"
    assert random.json()[0]["content"] == "Random message"