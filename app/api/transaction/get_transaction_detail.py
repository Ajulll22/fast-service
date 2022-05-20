from app.api_models.base_response import BaseResponseModel
from app.dependencies.get_db_session import get_db_session
from app.models.transaction import Transaction
from app.api_models.transaction_model import TransactionModel

import sqlalchemy as sa
from fastapi import Depends
from fastapi.exceptions import HTTPException


class GetTransactionDetailResponseModel(BaseResponseModel):
    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id': 10,
                    'created_at': '2022-05-20 21:00',
                    'status': 10,
                    'total': 400
                },
                'meta': {},
                'message': 'Success',
                'success': True,
                'code': 200
            }
        }


async def get_transaction_detail(transaction_id: int, session=Depends(get_db_session)):
    transaction = session.query(
        Transaction
    ).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(404, detail='Transaction not found')

    return GetTransactionDetailResponseModel(
        data=TransactionModel(
            id=transaction.id,
            created_at=transaction.created_at,
            status=transaction.status,
            total=transaction.total
        )
    )
