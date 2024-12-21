from flask import Blueprint, request, jsonify
from db import db
from models import Transaction, Chain, Token, Wallet

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([{
        'id': tx.id,
        'chain_id': tx.chain_id,
        'token_id': tx.token_id,
        'from_wallet_id': tx.from_wallet_id,
        'to_wallet_id': tx.to_wallet_id,
        'amount': str(tx.amount),
        'tx_hash': tx.tx_hash,
        'status': tx.status,
        'created_at': tx.created_at.isoformat(),
        'deleted_at': tx.deleted_at.isoformat() if tx.deleted_at else None
    } for tx in transactions])

@transactions_bp.route('/', methods=['POST'])
def create_transaction():
    data = request.get_json()
    required_fields = ('chain_id', 'from_wallet_id', 'to_wallet_id', 'amount', 'tx_hash')
    if not data or not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Validate chain
    chain = Chain.query.get(data['chain_id'])
    if not chain:
        return jsonify({'error': 'Chain not found'}), 404

    # Validate from_wallet and to_wallet
    from_wallet = Wallet.query.get(data['from_wallet_id'])
    to_wallet = Wallet.query.get(data['to_wallet_id'])
    if not from_wallet or not to_wallet:
        return jsonify({'error': 'From or To Wallet not found'}), 404

    # Validate token if provided
    token_id = data.get('token_id')
    if token_id:
        token = Token.query.get(token_id)
        if not token:
            return jsonify({'error': 'Token not found'}), 404

    # Check if tx_hash already exists
    existing_tx = Transaction.query.filter_by(tx_hash=data['tx_hash']).first()
    if existing_tx:
        return jsonify({'error': 'Transaction with this hash already exists.'}), 400

    new_transaction = Transaction(
        chain_id=data['chain_id'],
        token_id=token_id,
        from_wallet_id=data['from_wallet_id'],
        to_wallet_id=data['to_wallet_id'],
        amount=data['amount'],
        tx_hash=data['tx_hash'],
        status=data.get('status', 'pending')
    )
    db.session.add(new_transaction)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error creating transaction.'}), 400

    return jsonify({
        'id': new_transaction.id,
        'chain_id': new_transaction.chain_id,
        'token_id': new_transaction.token_id,
        'from_wallet_id': new_transaction.from_wallet_id,
        'to_wallet_id': new_transaction.to_wallet_id,
        'amount': str(new_transaction.amount),
        'tx_hash': new_transaction.tx_hash,
        'status': new_transaction.status,
        'created_at': new_transaction.created_at.isoformat(),
        'deleted_at': new_transaction.deleted_at
    }), 201
