def test_create_article(client):
    # Login as admin (first user is admin)
    client.post('/auth/register', json={
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'password'
    })
    client.post('/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })

    response = client.post('/api/articles', json={
        'title': 'Test Article',
        'content': 'This is a test article.',
        'summary': 'Test summary',
        'status': 'published'
    })
    assert response.status_code == 201
    assert b'Article created successfully' in response.data

def test_get_articles(client):
    response = client.get('/api/articles')
    assert response.status_code == 200
    assert b'articles' in response.data

def test_update_article(client):
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
    
    # Create article first (assuming ID 1)
    client.post('/api/articles', json={
        'title': 'To Update',
        'content': 'Content',
        'status': 'published'
    })

    response = client.put('/api/articles/1', json={
        'title': 'Updated Title'
    })
    assert response.status_code == 200
    
    # Verify update
    response = client.get('/api/articles/1')
    assert b'Updated Title' in response.data

def test_delete_article(client):
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

    # Create article first
    client.post('/api/articles', json={
        'title': 'To Delete',
        'content': 'Content',
        'status': 'published'
    })

    response = client.delete('/api/articles/1')
    assert response.status_code == 200
