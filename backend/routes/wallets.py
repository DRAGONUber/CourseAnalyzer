from flask import Blueprint, request, jsonify
from db import db
from models import Wallet, Chain, MasterKey, Token

wallets_bp = Blueprint('wallets', __name__)

@wallets_bp.route('/', methods=['GET'])
def get_wallets():
    wallets = Wallet.query.all()
    return jsonify([{
        'id': wallet.id,
        'chain_id': wallet.chain_id,
        'master_key_id': wallet.master_key_id,
        'wallet_public_key': wallet.wallet_public_key,
        'transaction_session_id': wallet.transaction_session_id,
        'created_at': wallet.created_at.isoformat(),
        'iws_id': wallet.iws_id,
        'token_addresses': wallet.token_addresses
    } for wallet in wallets])

@wallets_bp.route('/', methods=['POST'])
def create_wallet():
    data = request.get_json()
    required_fields = ('chain_id', 'master_key_id', 'wallet_public_key', 'transaction_session_id', 'iws_id', 'token_addresses')
    if not data or not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the associated chain exists
    chain = Chain.query.get(data['chain_id'])
    if not chain:
        return jsonify({'error': 'Chain not found'}), 404

    # Check if the associated master_key exists
    master_key = MasterKey.query.get(data['master_key_id'])
    if not master_key:
        return jsonify({'error': 'MasterKey not found'}), 404

    new_wallet = Wallet(
        chain_id=data['chain_id'],
        master_key_id=data['master_key_id'],
        wallet_public_key=data['wallet_public_key'],
        transaction_session_id=data['transaction_session_id'],
        iws_id=data['iws_id'],
        token_addresses=data['token_addresses']
    )
    db.session.add(new_wallet)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Wallet with this public key already exists.'}), 400

    return jsonify({
        'id': new_wallet.id,
        'chain_id': new_wallet.chain_id,
        'master_key_id': new_wallet.master_key_id,
        'wallet_public_key': new_wallet.wallet_public_key,
        'transaction_session_id': new_wallet.transaction_session_id,
        'created_at': new_wallet.created_at.isoformat(),
        'iws_id': new_wallet.iws_id,
        'token_addresses': new_wallet.token_addresses
    }), 201
