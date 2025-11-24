from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Setting

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')

@settings_bp.route('', methods=['GET'])
def get_settings():
    # Public settings? Or only admin?
    # Usually some settings are public (site title), some private.
    # For simplicity, let's return all for now, or filter if needed.
    # Let's assume all settings stored here are public-safe or we filter keys.
    settings = Setting.query.all()
    result = {s.key: s.value for s in settings}
    return jsonify(result)

@settings_bp.route('', methods=['POST'])
@login_required
def update_settings():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    # Expecting a dict of key-values
    
    for key, value in data.items():
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            setting.value = str(value)
        else:
            setting = Setting(key=key, value=str(value))
            db.session.add(setting)
            
    db.session.commit()
    return jsonify({'message': 'Settings updated successfully'})
