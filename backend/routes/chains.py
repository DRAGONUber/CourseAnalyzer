from flask import Blueprint, request, jsonify
from db import db
from models import Chain

chains_bp = Blueprint('chains', __name__)

@chains_bp.route('/', methods=['GET'])
def get_chains():
    chains = Chain.query.all()
    return jsonify([{
        'id': chain.id,
        'chain_name': chain.chain_name,
        'chain_type': chain.chain_type,
        'created_at': chain.created_at.isoformat(),
        'deleted_at': chain.deleted_at.isoformat() if chain.deleted_at else None
    } for chain in chains])

@chains_bp.route('/', methods=['POST'])
def create_chain():
    data = request.get_json()
    if not data or not all(k in data for k in ('chain_name', 'chain_type')):
        return jsonify({'error': 'Missing required fields'}), 400

    new_chain = Chain(
        chain_name=data['chain_name'],
        chain_type=data['chain_type']
    )
    db.session.add(new_chain)
    db.session.commit()

    return jsonify({
        'id': new_chain.id,
        'chain_name': new_chain.chain_name,
        'chain_type': new_chain.chain_type,
        'created_at': new_chain.created_at.isoformat(),
        'deleted_at': new_chain.deleted_at
    }), 201
