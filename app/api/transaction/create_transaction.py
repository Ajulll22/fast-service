from fastapi import Header, Depends
from fastapi.exceptions import HTTPException

from app.api_models.base_response import BaseResponseModel
from app.models.transaction import Transaction
from app.dependencies.get_db_session import get_db_session


class CreateTransactionResponseModel(BaseResponseModel):

    class Config:
        schema_extra = {
            'example': {
                'data': {
                    'id': 10,
                    'url': '/api/v1/transaction/10',
                },
                'meta': {},
                'message': 'Success',
                'success': True,
                'code': 200
            }
        }


async def create_transaction(user_id: int = Header(0, alias='X-Consumer-ID'), session=Depends(get_db_session)):
    if user_id == 0:
        raise HTTPException(403, detail='Unauthorize')

    transaction = Transaction(user_id=user_id)
    session.add(transaction)
    session.commit()

    return CreateTransactionResponseModel(
        data={
            'id': transaction.id,
            'url': f'/api/v1/transaction/{transaction.id}'
        }
    )
