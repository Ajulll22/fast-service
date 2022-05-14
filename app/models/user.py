from app.models import Base
import sqlalchemy as sa

class User(Base):
    __tablename__ = 'user'
    id = sa.Column('id', sa.Integer, primary_key=True)
    username = sa.Column('username', sa.String)
    password = sa.Column('password', sa.String)
    full_name = sa.Column('full_name', sa.String)
    created_at = sa.Column('created_at', sa.DateTime, default=sa.func.NOW())
    modified_at = sa.Column('modified_at', sa.DateTime, default=sa.func.NOW(), onupdate=sa.func.NOW())