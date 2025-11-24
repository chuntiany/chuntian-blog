def test_get_settings(client):
    response = client.get('/api/settings')
    assert response.status_code == 200
    assert response.json == {}

def test_update_settings(client):
    # Register and login as admin
    client.post('/auth/register', json={
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'password'
    })
    client.post('/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })

    response = client.post('/api/settings', json={
        'site_title': 'My Blog',
        'allow_comments': 'true'
    })
    assert response.status_code == 200
    
    # Verify update
    response = client.get('/api/settings')
    assert response.json['site_title'] == 'My Blog'
    assert response.json['allow_comments'] == 'true'
