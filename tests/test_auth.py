def test_register(client):
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_login(client):
    # Register first
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Login
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data

def test_login_invalid(client):
    response = client.post('/auth/login', json={
        'username': 'wronguser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
