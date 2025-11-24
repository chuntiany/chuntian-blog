from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Comment, Article

comment_bp = Blueprint('comment', __name__, url_prefix='/api/comments')

@comment_bp.route('', methods=['POST'])
@login_required
def create_comment():
    data = request.get_json()
    content = data.get('content')
    article_id = data.get('article_id')

    if not content or not article_id:
        return jsonify({'error': 'Missing required fields'}), 400

    article = db.session.get(Article, article_id)
    if not article:
        return jsonify({'error': 'Article not found'}), 404

    # Default status: pending if admin approval required (TODO: check settings), else approved
    # For now, let's say default is pending
    status = 'pending'
    if current_user.is_admin:
        status = 'approved'

    comment = Comment(
        content=content,
        article_id=article_id,
        user_id=current_user.id,
        status=status
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Comment submitted successfully', 'id': comment.id, 'status': status}), 201

@comment_bp.route('', methods=['GET'])
def get_comments():
    # Admin sees all, User sees approved or own?
    # Usually public endpoint for article comments, admin endpoint for all.
    # Let's support filtering by article_id and status.
    
    article_id = request.args.get('article_id')
    status = request.args.get('status')
    
    query = Comment.query

    if article_id:
        query = query.filter_by(article_id=article_id)
    
    if status:
        query = query.filter_by(status=status)
    elif not current_user.is_authenticated or not current_user.is_admin:
        # Public only sees approved
        query = query.filter_by(status='approved')

    comments = query.order_by(Comment.created_at.desc()).all()
    
    result = []
    for comment in comments:
        result.append({
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'status': comment.status,
            'author': comment.author.username,
            'article_id': comment.article_id
        })
    return jsonify(result)

@comment_bp.route('/<int:id>/status', methods=['PUT'])
@login_required
def update_comment_status(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    comment = Comment.query.get_or_404(id)
    data = request.get_json()
    status = data.get('status')
    
    if status not in ['approved', 'rejected', 'pending']:
        return jsonify({'error': 'Invalid status'}), 400
        
    comment.status = status
    db.session.commit()
    return jsonify({'message': 'Comment status updated successfully'})

@comment_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_comment(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'})
