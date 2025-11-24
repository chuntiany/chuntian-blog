from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Article, Category

article_bp = Blueprint('article', __name__, url_prefix='/api/articles')

@article_bp.route('', methods=['POST'])
@login_required
def create_article():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    summary = data.get('summary')
    category_id = data.get('category_id')
    status = data.get('status', 'published')

    if not title or not content:
        return jsonify({'error': 'Missing required fields'}), 400

    article = Article(
        title=title,
        content=content,
        summary=summary,
        category_id=category_id,
        status=status,
        author=current_user
    )

    db.session.add(article)
    db.session.commit()

    return jsonify({'message': 'Article created successfully', 'id': article.id}), 201

@article_bp.route('', methods=['GET'])
def get_articles():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    query = Article.query
    
    if status:
        query = query.filter_by(status=status)
    elif not current_user.is_authenticated or not current_user.is_admin:
        # Public only sees published
        query = query.filter_by(status='published')

    pagination = query.order_by(Article.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    articles = []
    for article in pagination.items:
        articles.append({
            'id': article.id,
            'title': article.title,
            'summary': article.summary,
            'created_at': article.created_at.isoformat(),
            'status': article.status,
            'author': article.author.username,
            'category': article.category.name if article.category else None
        })

    return jsonify({
        'articles': articles,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@article_bp.route('/<int:id>', methods=['GET'])
def get_article(id):
    article = Article.query.get_or_404(id)
    
    if article.status != 'published':
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'summary': article.summary,
        'created_at': article.created_at.isoformat(),
        'status': article.status,
        'author': article.author.username,
        'category': article.category.name if article.category else None,
        'category_id': article.category_id
    })

@article_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_article(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    article = Article.query.get_or_404(id)
    data = request.get_json()
    
    article.title = data.get('title', article.title)
    article.content = data.get('content', article.content)
    article.summary = data.get('summary', article.summary)
    article.category_id = data.get('category_id', article.category_id)
    article.status = data.get('status', article.status)

    db.session.commit()
    return jsonify({'message': 'Article updated successfully'})

@article_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_article(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': 'Article deleted successfully'})
