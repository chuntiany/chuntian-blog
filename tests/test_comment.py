def test_create_comment(client):
    # Register admin first (so it gets is_admin=True)
    client.post('/auth/register', json={
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'password'
    })
    
    # Register user
    client.post('/auth/register', json={
        'username': 'user',
        'email': 'user@example.com',
        'password': 'password'
    })

    # Login admin to create article
    client.post('/auth/login', json={
        'username': 'admin',
        'password': 'password'
    })
    
    response = client.post('/api/articles', json={
        'title': 'Commentable Article',
        'content': 'Content',
        'status': 'published'
    })
    assert response.status_code == 201
    article_id = response.json['id']
    
    # Login user again
    client.post('/auth/login', json={
        'username': 'user',
        'password': 'password'
    })

    response = client.post('/api/comments', json={
        'content': 'Nice post!',
        'article_id': article_id
    })
    assert response.status_code == 201
    assert b'Comment submitted successfully' in response.data

def test_get_comments(client):
    response = client.get('/api/comments')
    assert response.status_code == 200
    assert b'[]' in response.data

def test_update_comment_status(client):
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
    
    # Create article
    client.post('/api/articles', json={
        'title': 'Article',
        'content': 'Content',
        'status': 'published'
    })
    
    # Create comment (as admin, so auto-approved, but let's update it)
    client.post('/api/comments', json={
        'content': 'Comment',
        'article_id': 1
    })

    response = client.put('/api/comments/1/status', json={
        'status': 'rejected'
    })
    assert response.status_code == 200
    
    # Verify update
    response = client.get('/api/comments?status=rejected')
    assert b'Comment' in response.data

def test_delete_comment(client):
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

    # Create article & comment
    client.post('/api/articles', json={
        'title': 'Article',
        'content': 'Content',
        'status': 'published'
    })
    client.post('/api/comments', json={
        'content': 'To Delete',
        'article_id': 1
    })

    response = client.delete('/api/comments/1')
    assert response.status_code == 200
