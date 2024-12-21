from flask import Blueprint, request, jsonify
from db import db
from models import Token, Chain

tokens_bp = Blueprint('tokens', __name__)

@tokens_bp.route('/', methods=['GET'])
def get_tokens():
    tokens = Token.query.all()
    return jsonify([{
        'id': token.id,
        'chain_id': token.chain_id,
        'token_name': token.token_name,
        'contract_address': token.contract_address,
        'created_at': token.created_at.isoformat(),
        'deleted_at': token.deleted_at.isoformat() if token.deleted_at else None
    } for token in tokens])

@tokens_bp.route('/', methods=['POST'])
def create_token():
    data = request.get_json()
    if not data or not all(k in data for k in ('chain_id', 'token_name', 'contract_address')):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the associated chain exists
    chain = Chain.query.get(data['chain_id'])
    if not chain:
        return jsonify({'error': 'Chain not found'}), 404

    new_token = Token(
        chain_id=data['chain_id'],
        token_name=data['token_name'],
        contract_address=data['contract_address']
    )
    db.session.add(new_token)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Token with this chain_id and contract_address already exists.'}), 400

    return jsonify({
        'id': new_token.id,
        'chain_id': new_token.chain_id,
        'token_name': new_token.token_name,
        'contract_address': new_token.contract_address,
        'created_at': new_token.created_at.isoformat(),
        'deleted_at': new_token.deleted_at
    }), 201
