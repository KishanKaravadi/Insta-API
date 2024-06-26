import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users/", json={'email': 'example@gmail.com', 'password': 'password'})
    new_user = schemas.User(**res.json())
    assert new_user.email == 'example@gmail.com'
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={'username': test_user['email'], 'password': test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, [settings.algorithm])
    id_num = payload.get("user_id")
    assert id_num == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', 'password', 403),
    ('example@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password', 422),
    ('example@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        '/login', data={'username': email, 'password': password})

    assert res.status_code == status_code
