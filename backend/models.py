from db import db

class Chain(db.Model):
    __tablename__ = 'chains'
    id = db.Column(db.Integer, primary_key=True)
    chain_name = db.Column(db.Text, nullable=False)
    chain_type = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    master_keys = db.relationship('MasterKey', backref='chain', cascade='all, delete-orphan')
    tokens = db.relationship('Token', backref='chain', cascade='all, delete-orphan')
    wallets = db.relationship('Wallet', backref='chain', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='chain', cascade='all, delete-orphan')


class MasterKey(db.Model):
    __tablename__ = 'master_keys'
    id = db.Column(db.Integer, primary_key=True)
    chain_id = db.Column(db.Integer, db.ForeignKey('chains.id', ondelete='SET NULL'), nullable=True)
    keystore_key_name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('chain_id', 'keystore_key_name', name='_chain_keystore_uc'),
    )


class Token(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    chain_id = db.Column(db.Integer, db.ForeignKey('chains.id', ondelete='SET NULL'), nullable=True)
    token_name = db.Column(db.Text, nullable=False)
    contract_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('chain_id', 'contract_address', name='_chain_contract_uc'),
    )


class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    chain_id = db.Column(db.Integer, db.ForeignKey('chains.id', ondelete='SET NULL'), nullable=True)
    master_key_id = db.Column(db.Integer, db.ForeignKey('master_keys.id', ondelete='SET NULL'), nullable=True)
    wallet_public_key = db.Column(db.Text, nullable=False, unique=True)
    transaction_session_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    iws_id = db.Column(db.Text, nullable=False)
    token_addresses = db.Column(db.JSON, nullable=False)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    chain_id = db.Column(db.Integer, db.ForeignKey('chains.id'), nullable=False)  # Added ForeignKey
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.id'), nullable=True)
    from_wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)  # Added ForeignKey
    to_wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)    # Added ForeignKey
    amount = db.Column(db.Numeric(38, 18), nullable=False)
    tx_hash = db.Column(db.Text, nullable=False, unique=True)
    status = db.Column(db.Text, nullable=False, default='pending')
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    __table_args__ = (
        db.CheckConstraint("status IN ('pending', 'confirmed', 'failed')", name='check_status'),
        db.CheckConstraint('from_wallet_id <> to_wallet_id', name='check_wallets_different'),
    )


class GradeDistribution(db.Model):
    __tablename__ = 'grade_distribution'
    
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    course_subject = db.Column(db.String(10), nullable=False)
    course_number = db.Column(db.String(10), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    grade_a = db.Column(db.Integer)
    grade_b = db.Column(db.Integer)
    grade_c = db.Column(db.Integer)
    grade_d = db.Column(db.Integer)
    grade_f = db.Column(db.Integer)
    
    def __repr__(self):
        return f"<GradeDistribution {self.course_subject} {self.course_number} - {self.instructor}>"
