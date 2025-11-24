from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Category

category_bp = Blueprint('category', __name__, url_prefix='/api/categories')

@category_bp.route('', methods=['POST'])
@login_required
def create_category():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Missing required fields'}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'Category already exists'}), 400

    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category created successfully', 'id': category.id}), 201

@category_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'article_count': category.articles.count()
        })
    return jsonify(result)

@category_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_category(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    name = data.get('name')
    if name and name != category.name:
        if Category.query.filter_by(name=name).first():
            return jsonify({'error': 'Category name already exists'}), 400
        category.name = name
        
    category.description = data.get('description', category.description)
    db.session.commit()
    return jsonify({'message': 'Category updated successfully'})

@category_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_category(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    category = Category.query.get_or_404(id)
    
    # Check if category has articles?
    # For now, let's allow deletion, but articles will have category_id=NULL (if nullable) or cascade?
    # In models.py: category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # Default is restrict or set null depending on DB. SQLAlchemy default is usually nothing (error).
    # Let's check if it has articles.
    if category.articles.count() > 0:
        return jsonify({'error': 'Cannot delete category with articles'}), 400

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'})
