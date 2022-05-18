from app.models import Base

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import TINYINT


class Product(Base):
    __tablename__ = 'product'

    id = sa.Column('id', sa.Integer, primary_key=True)
    barcode = sa.Column('barcode', sa.String)
    name = sa.Column('name', sa.String)
    price = sa.Column('price', sa.Integer)
    is_active = sa.Column('is_active', TINYINT)
    created_at = sa.Column('created_at', sa.DateTime, default=sa.func.NOW())
    modified_at = sa.Column('modified_at', sa.DateTime,
                            default=sa.func.NOW(), onupdate=sa.func.NOW())
