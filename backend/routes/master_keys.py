from flask import Blueprint, request, jsonify
from db import db
from models import MasterKey, Chain

master_keys_bp = Blueprint('master_keys', __name__)

@master_keys_bp.route('/', methods=['GET'])
def get_master_keys():
    master_keys = MasterKey.query.all()
    return jsonify([{
        'id': mk.id,
        'chain_id': mk.chain_id,
        'keystore_key_name': mk.keystore_key_name,
        'created_at': mk.created_at.isoformat(),
        'deleted_at': mk.deleted_at.isoformat() if mk.deleted_at else None
    } for mk in master_keys])

@master_keys_bp.route('/', methods=['POST'])
def create_master_key():
    data = request.get_json()
    if not data or not all(k in data for k in ('chain_id', 'keystore_key_name')):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the associated chain exists
    chain = Chain.query.get(data['chain_id'])
    if not chain:
        return jsonify({'error': 'Chain not found'}), 404

    new_master_key = MasterKey(
        chain_id=data['chain_id'],
        keystore_key_name=data['keystore_key_name']
    )
    db.session.add(new_master_key)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'MasterKey with this chain_id and keystore_key_name already exists.'}), 400

    return jsonify({
        'id': new_master_key.id,
        'chain_id': new_master_key.chain_id,
        'keystore_key_name': new_master_key.keystore_key_name,
        'created_at': new_master_key.created_at.isoformat(),
        'deleted_at': new_master_key.deleted_at
    }), 201
