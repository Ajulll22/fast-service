from app.api_models.base_response import BaseResponseModel
from app.dependencies.get_db_session import get_db_session
from app.models.transaction_item import TransactionItem
from app.models.transaction import Transaction, TransactionStatus
from app.models.product import Product

from fastapi import Header, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
import sqlalchemy as sa


class CreateTransactionItemData(BaseModel):
    transaction_id: int
    product_id: int
    qty: int


class CreateTransactionItemResponseModel(BaseResponseModel):
    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id': 10,
                    'url': '/api/v1/transaction-item/10',
                },
                'meta': {},
                'message': 'Success',
                'success': True,
                'code': 200
            }
        }


async def create_transaction_item(data: CreateTransactionItemData, user_id: int = Header(0, alias='X-Consumer-ID'), session=Depends(get_db_session)):
    if user_id == 0:
        raise HTTPException(403, detail='Unauthorize')

    transaction = session.query(
        Transaction.id, Transaction.status
    ).filter(
        Transaction.id == data.transaction_id
    ).first()

    if not transaction:
        raise HTTPException(400, detail='Transaction Not Found')

    if transaction.status > TransactionStatus.OUTSTANDING:
        raise HTTPException(
            400, detail='Transaction has been complete, cant add more item')

    # check product
    product = session.query(
        Product.id, Product.name, Product.price
    ).filter(
        Product.id == data.product_id
    ).filter(
        Product.is_active
    ).first()

    if not product:
        raise HTTPException(400, detail='Product Not Found')

    total = product.price * data.qty

    transaction_item = TransactionItem(
        user_id=user_id,
        transaction_id=data.transaction_id,
        product_id=data.product_id,
        product_name=product.name,
        price=product.price,
        qty=data.qty,
        total=total
    )

    session.add(transaction_item)

    # add total transaction
    session.execute(
        sa.update(Transaction).values(
            total=Transaction.total + total
        ).where(
            Transaction.id == data.transaction_id
        )
    )

    session.commit()

    return CreateTransactionItemResponseModel(
        data={
            'id': transaction_item.id,
            'url': f'/api/v1/transaction-item/{transaction_item.id}'
        }
    )
