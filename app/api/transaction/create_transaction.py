from fastapi import Header

from app.api_models.base_response import BaseResponseModel


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


async def create_transaction(user_id: int = Header(0, alias='X-Consumer-ID')):
    pass
