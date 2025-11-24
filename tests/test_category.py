def test_create_category(client):
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

    response = client.post('/api/categories', json={
        'name': 'Tech',
        'description': 'Technology news'
    })
    assert response.status_code == 201
    assert b'Category created successfully' in response.data

def test_get_categories(client):
    response = client.get('/api/categories')
    assert response.status_code == 200
    assert b'[]' in response.data

def test_update_category(client):
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
    
    # Create category
    client.post('/api/categories', json={
        'name': 'Old Name',
        'description': 'Desc'
    })

    response = client.put('/api/categories/1', json={
        'name': 'New Name'
    })
    assert response.status_code == 200
    
    # Verify update
    response = client.get('/api/categories')
    assert b'New Name' in response.data

def test_delete_category(client):
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

    # Create category
    client.post('/api/categories', json={
        'name': 'To Delete',
        'description': 'Desc'
    })

    response = client.delete('/api/categories/1')
    assert response.status_code == 200
