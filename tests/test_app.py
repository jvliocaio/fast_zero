from fast_zero.schemas import UserPublic


def test_root_deve_retornar_200_e_ola_mundo(client):

    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):

    response = client.post(
        '/users',
        json={
            'username': 'jvlio',
            'email': 'jvlio@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'username': 'jvlio',
        'email': 'jvlio@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):

    user_id = user.id

    if user_id is None:
        response = client.put(
            '/users/{}'.format(user_id),
            json={
                'username': 'bob',
                'email': 'bob@example.com',
                'password': 'mynewpassword',
            },
        )
        assert response.status_code == 404
        assert response.json() == {'detail': 'User not found'}

    else:
        response = client.put(
            '/users/{}'.format(user_id),
            json={
                'username': 'bob',
                'email': 'bob@example.com',
                'password': 'mynewpassword',
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            'username': 'bob',
            'email': 'bob@example.com',
            'id': 1,
        }


def test_delete_user(client, user):

    user_id = user.id

    if user_id is None:
        response = client.delete('/users/{}'.format(user_id))
        assert response.status_code == 404
        assert response.json() == {'detail': 'User not found'}

    else:
        response = client.delete('/users/{}'.format(user_id))
        assert response.status_code == 200
        assert response.json() == {'detail': 'User deleted'}
